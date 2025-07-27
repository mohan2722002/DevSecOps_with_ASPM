import requests
import os
import sys

# Map file names to DefectDojo scan types
SCAN_TYPE_MAP = {
    'gitleaks-report.json': 'Gitleaks Scan',
    'report.json': 'Trivy Scan',  # This is from trivy-sca
    'snyk-report.json': 'Snyk Scan',
    'zap-report.json': 'ZAP Scan',
}

def determine_scan_type(report_path):
    file_name = os.path.basename(report_path).lower()
    
    # Check for exact filename matches first
    if file_name in SCAN_TYPE_MAP:
        return SCAN_TYPE_MAP[file_name]
    
    # Check for keyword matches in filename
    if 'gitleaks' in file_name:
        return 'Gitleaks Scan'
    elif 'snyk' in file_name:
        return 'Snyk Scan'
    elif 'zap' in file_name:
        return 'ZAP Scan'
    elif 'trivy' in file_name or file_name == 'report.json':
        return 'Trivy Scan'
    
    # Default fallback - should not happen with proper naming
    return 'Trivy Scan'

def upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path):
    headers = {'Authorization': f'Token {api_key}'}
    
    with open(report_path, 'rb') as f:
        files = {
            'file': (os.path.basename(report_path), f, 'application/json')
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
        print(f'✅ Successfully uploaded {report_path} as {scan_type}')
    else:
        print(f'❌ Failed to upload {report_path} as {scan_type} - {response.status_code}: {response.text}')

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
        print(f'📄 Processing {report_path} as {scan_type}')
        upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path)

if __name__ == '__main__':
    main()