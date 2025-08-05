import requests
import os
import sys

# Map file names to DefectDojo scan types
SCAN_TYPE_MAP = {
    'gitleaks-report.json': 'Gitleaks Scan',
    'sca_report.json': 'Trivy Scan',
    'snyk-report.json': 'Snyk Scan',
    'dast_report.xml': 'ZAP Scan',
    'image_scan_report.json': 'Trivy Scan',
    'container_scan_report.json': 'Trivy Scan',
}

def determine_scan_type(report_path):
    file_name = os.path.basename(report_path).lower()
    
    if file_name in SCAN_TYPE_MAP:
        return SCAN_TYPE_MAP[file_name]
    
    if 'gitleaks' in file_name:
        return 'Gitleaks Scan'
    elif 'snyk' in file_name:
        return 'Snyk Scan'
    elif 'dast' in file_name:
        return 'ZAP Scan'
    elif 'sca' in file_name:
        return 'Trivy Scan'
    elif 'image' in file_name:
        return 'Trivy Scan'
    elif 'container' in file_name:
        return 'Trivy Scan'

    return 'Unknown Scan Type'

def get_tag_from_filename(report_path):
    file_name = os.path.basename(report_path).lower()

    if 'image' in file_name:
        return 'image'
    elif 'sca' in file_name:
        return 'sca'
    elif 'container' in file_name:
        return 'runtime'
    elif 'gitleaks' in file_name:
        return 'secret-scan'
    elif 'snyk' in file_name:
        return 'sast'
    elif 'dast' in file_name or file_name.endswith('.xml'):
        return 'dast'

    return 'default'

def upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path):
    headers = {'Authorization': f'Token {api_key}'}
    tag = get_tag_from_filename(report_path)

    with open(report_path, 'rb') as f:
        files = {
            'file': (os.path.basename(report_path), f, 'application/json')
        }
        data = {
            'engagement': engagement_id,
            'scan_type': scan_type,
            'active': 'true',
            'verified': 'true',
            'scan_date': '',
            'lead': '',
            'tags': tag,
        }
        
        url = f'{api_url}/api/v2/import-scan/'
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 201:
        print(f' Successfully uploaded {report_path} as {scan_type} with tag: {tag}')
    else:
        print(f' Failed to upload {report_path} as {scan_type} - {response.status_code}: {response.text}')

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
        print(f' Processing {report_path} as {scan_type}')
        upload_scan_report(api_url, api_key, engagement_id, scan_type, report_path)

if __name__ == '__main__':
    main()
