import requests
import base64
import re

# Short timeouts: (connect_timeout_sec, read_timeout_sec)
# Keeps the dashboard responsive even when GitHub is unreachable.
_CONNECT_TIMEOUT = 4
_READ_TIMEOUT = 8

SCAN_EXTENSIONS = {
    '.js', '.ts', '.py', '.java', '.go', '.cs', '.rb', '.php',
    '.swift', '.kt', '.vue', '.jsx', '.tsx', '.scala', '.rs',
}

SKIP_PATHS = {
    'node_modules/', 'vendor/', '.min.', 'dist/', 'build/',
    '__pycache__/', '.git/', 'coverage/', 'test/', 'spec/', 'tests/',
    '.github/', 'migrations/',
}


def parse_github_url(url):
    """Extract owner and repo name from a GitHub URL."""
    url = url.strip().rstrip('/').removesuffix('.git')
    match = re.match(
        r'https?://(?:www\.)?github\.com/([^/\s]+)/([^/\s]+)',
        url
    )
    if not match:
        return None, None
    return match.group(1), match.group(2)


def _default_result(repo_name=None, error=None):
    return {
        "risk_signals": {
            "validations": 0,
            "payment_logic": 0,
            "limit_checks": 0,
            "error_handling": 0,
            "auth_logic": 0,
            "data_logic": 0,
        },
        "scanned_files": [],
        "repo_name": repo_name,
        "total_files_scanned": 0,
        "error": error,
    }


def scan_github_repo(repo_url, token=None, max_files=40):
    """
    Scan a public GitHub repository for code risk signals.

    Args:
        repo_url: Full GitHub URL, e.g. https://github.com/owner/repo
        token:    Optional GitHub personal access token (for private repos / higher rate limits)
        max_files: Maximum number of source files to scan

    Returns:
        dict with keys: risk_signals, scanned_files, repo_name, total_files_scanned, error
    """
    if not repo_url or not repo_url.strip():
        return _default_result()

    owner, repo = parse_github_url(repo_url)
    if not owner:
        return _default_result(error=f"Invalid GitHub URL: {repo_url}")

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-QA-Engine/2.0',
    }
    if token:
        headers['Authorization'] = f'token {token}'

    # ── 1. Get repo info (to find the default branch) ─────────────────────────
    try:
        repo_resp = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}',
            headers=headers, timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT),
        )
    except requests.exceptions.RequestException as exc:
        msg = "GitHub unreachable — network timeout or connection refused"
        print(f"GitHub scan error: {exc}")
        return _default_result(repo_name=f"{owner}/{repo}", error=msg)

    if repo_resp.status_code == 404:
        return _default_result(
            repo_name=f"{owner}/{repo}",
            error=f"Repository {owner}/{repo} not found or is private",
        )
    if repo_resp.status_code != 200:
        return _default_result(
            repo_name=f"{owner}/{repo}",
            error=f"GitHub API error: {repo_resp.status_code}",
        )

    default_branch = repo_resp.json().get('default_branch', 'main')

    # ── 2. Fetch the recursive file tree ──────────────────────────────────────
    try:
        tree_resp = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1',
            headers=headers, timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT),
        )
    except requests.exceptions.RequestException as exc:
        msg = "GitHub unreachable — network timeout or connection refused"
        print(f"GitHub scan error: {exc}")
        return _default_result(repo_name=f"{owner}/{repo}", error=msg)

    if tree_resp.status_code != 200:
        return _default_result(
            repo_name=f"{owner}/{repo}",
            error="Could not fetch repository file tree",
        )

    tree = tree_resp.json().get('tree', [])

    # ── 3. Filter to scannable source files ───────────────────────────────────
    files_to_scan = []
    for entry in tree:
        if entry['type'] != 'blob':
            continue
        path = entry['path']
        if any(skip in path for skip in SKIP_PATHS):
            continue
        if not any(path.endswith(ext) for ext in SCAN_EXTENSIONS):
            continue
        files_to_scan.append(path)
        if len(files_to_scan) >= max_files:
            break

    # ── 4. Scan each file ─────────────────────────────────────────────────────
    risk_signals = {
        "validations": 0,
        "payment_logic": 0,
        "limit_checks": 0,
        "error_handling": 0,
        "auth_logic": 0,
        "data_logic": 0,
    }
    scanned_files = []

    for file_path in files_to_scan:
        try:
            content_resp = requests.get(
                f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={default_branch}',
                headers=headers, timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT),
            )
        except requests.exceptions.RequestException:
            continue

        if content_resp.status_code != 200:
            continue

        content_data = content_resp.json()
        if content_data.get('encoding') != 'base64':
            continue

        try:
            content = base64.b64decode(content_data['content']).decode('utf-8', errors='ignore').lower()
        except Exception:
            continue

        scanned_files.append(file_path)

        if any(k in content for k in [
            'validate', 'validation', 'required', 'mandatory',
            'assert', 'constraint', 'isvalid', 'isrequired',
        ]):
            risk_signals["validations"] += 1

        if any(k in content for k in [
            'payment', 'fee', 'charge', 'price', 'amount', 'calculate',
            'total', 'billing', 'invoice', 'sst', 'tax', 'cost', 'rate',
            'checkout', 'refund', 'wallet',
        ]):
            risk_signals["payment_logic"] += 1

        if any(k in content for k in [
            'limit', 'threshold', 'max', 'minimum', 'quota',
            'exceed', 'boundary', 'cap', 'maximum', 'min_',
        ]):
            risk_signals["limit_checks"] += 1

        if any(k in content for k in [
            'error', 'exception', 'throw', 'catch', 'fail',
            'retry', 'fallback', 'handle', 'onerror', 'reject',
        ]):
            risk_signals["error_handling"] += 1

        if any(k in content for k in [
            'auth', 'login', 'token', 'session', 'password',
            'permission', 'role', 'jwt', 'oauth', 'authorize', 'authenticate',
        ]):
            risk_signals["auth_logic"] += 1

        if any(k in content for k in [
            'database', 'query', 'insert', 'update', 'delete',
            'transaction', 'commit', 'rollback', 'sql', 'orm',
            'model', 'repository', 'entity',
        ]):
            risk_signals["data_logic"] += 1

    print(f"GitHub Scan: {owner}/{repo} — {len(scanned_files)} files scanned")
    print(f"Risk Signals: {risk_signals}")

    return {
        "risk_signals": risk_signals,
        "scanned_files": scanned_files,
        "repo_name": f"{owner}/{repo}",
        "total_files_scanned": len(scanned_files),
        "error": None,
    }
