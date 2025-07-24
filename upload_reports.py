import requests
import os
import sys

# Map file names to DefectDojo scan types
SCAN_TYPE_MAP = {
    'gitleaks': 'Gitleaks Scan',
    'trivy': 'Trivy Scan',
    'snyk': 'Snyk Scan',
    'zap': 'OWASP ZAP Scan',
    # Extend as needed for more tools
}

def determine_scan_type(report_path):
    file_name = os.path.basename(report_path).lower()
    for keyword, scan_type in SCAN_TYPE_MAP.items():
        if keyword in file_name:
            return scan_type
    return 'Generic Scan'  # Fallback

def upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path):
    headers = {'Authorization': f'Token {api_key}'}
    files = {
        'file': (os.path.basename(report_path), open(report_path, 'rb'), 'application/json')
    }
    data = {
        'engagement': engagement_id,
        'scan_type': scan_type,
        'active': 'true',
        'verified': 'true',
        'scan_date': '',  # Optional: Provide if available
        'lead': '',       # Optional: DefectDojo user ID or email
        'tags': '',       # Optional: Any custom tags
    }
    url = f'{api_url}/api/v2/import-scan/'
    response = requests.post(url, headers=headers, files=files, data=data)
    if response.status_code == 201:
        print(f'Successfully uploaded {report_path} as {scan_type}')
    else:
        print(f'Failed to upload {report_path} - {response.status_code}: {response.text}')

def main():
    if len(sys.argv) < 2:
        print('Usage: python upload_reports.py <report-file1> [<report-file2> ...]')
        return
    api_url = os.getenv('DEFECTDOJO_API_URL')
    api_key = os.getenv('DEFECTDOJO_API_KEY')
    engagement_id = os.getenv('DEFECTDOJO_ENGAGEMENT_ID')
    if not api_url or not api_key or not engagement_id:
        print('Please set DEFECTDOJO_API_URL, DEFECTDOJO_API_KEY, and DEFECTDOJO_ENGAGEMENT_ID environment variables.')
        return
    report_files = sys.argv[1:]
    for report_path in report_files:
        if not os.path.isfile(report_path):
            print(f'File not found: {report_path}')
            continue
        scan_type = determine_scan_type(report_path)
        upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path)

if __name__ == '__main__':
    main()
