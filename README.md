# DevSecOps Security Pipeline

A comprehensive automated security testing pipeline that integrates multiple security scanning tools across the entire software development lifecycle.

## Overview

This project implements a complete DevSecOps pipeline that performs automated security scanning at every stage of the development process. The pipeline integrates eight distinct security scanning stages, from secret detection to dynamic application security testing, with automated reporting to DefectDojo for centralized vulnerability management.

## Pipeline Architecture

The security pipeline is structured into eight sequential stages, each targeting specific security aspects:
[](https://cdn.corenexis.com/file?8226399168.png)
```
Secret Scan → SCA → SAST → Building → Image Scan → Container Security → DAST → Upload Results
```

## Pipeline Execution Workflow

The pipeline is triggered automatically on code commits and executes the following workflow:

1. Source code is checked out and prepared for scanning
2. Security scans are performed in parallel where possible
3. Application is built and deployed for dynamic testing
4. All security findings are collected and normalized
5. Results are uploaded to DefectDojo for centralized tracking

## Technology Stack

### Security Tools
- **GitLeaks**: Secret detection and credential scanning
- **Trivy**: Vulnerability scanning for containers and filesystems
- **Snyk**: Static code analysis and dependency vulnerability detection
- **OWASP ZAP**: Dynamic application security testing
- **DefectDojo**: Centralized vulnerability management platform

### Infrastructure
- **GitLab CI/CD**: Pipeline orchestration and execution
- **Docker**: Containerization and image management
- **Python**: Custom scripting for report handling and API integration

## Integration Points

The pipeline integrates with multiple external systems:

- **Version Control**: GitLab repository for source code management
- **Container Registry**: Docker Hub and private registries for image storage
- **Vulnerability Database**: Multiple CVE databases through integrated tools
- **Security Platform**: DefectDojo for centralized vulnerability management

## Pipeline Stages

### 1. Secret Scanning
- **Tool Used**: GitLeaks
- **Purpose**: Source code is scanned for hardcoded secrets, API keys, and sensitive credentials
- **Output**: JSON report containing detected secrets and their locations
- **Implementation**: The entire repository is analyzed using GitLeaks' detection engine with verbose logging enabled

### 2. Software Composition Analysis (SCA)
- **Tool Used**: Trivy
- **Purpose**: Dependencies and third-party libraries are analyzed for known vulnerabilities
- **Output**: Comprehensive JSON report of vulnerable components
- **Implementation**: The file system is scanned to identify all dependencies and cross-referenced against vulnerability databases

### 3. Static Application Security Testing (SAST)
- **Tool Used**: Snyk
- **Purpose**: Source code is analyzed for security vulnerabilities and coding flaws
- **Output**: JSON report with identified code-level security issues
- **Implementation**: Code is authenticated with Snyk and analyzed for security patterns and anti-patterns

### 4. Application Building
- **Tool Used**: Docker Compose
- **Purpose**: Application containers are built from source code
- **Output**: Docker images ready for deployment
- **Implementation**: Multi-container applications are built using Docker Compose configuration files

### 5. Container Image Scanning
- **Tool Used**: Trivy
- **Purpose**: Built Docker images are scanned for vulnerabilities in base images and installed packages
- **Output**: Individual JSON reports for each scanned image
- **Implementation**: All built images are identified and scanned for HIGH and CRITICAL severity vulnerabilities

### 6. Container Runtime Security
- **Tool Used**: Trivy
- **Purpose**: Running containers are assessed for runtime security risks
- **Output**: Real-time security assessment of active containers
- **Implementation**: Currently running containers are inspected and their base images are security-scanned

### 7. Dynamic Application Security Testing (DAST)
- **Tool Used**: OWASP ZAP
- **Output**: HTML and JSON reports containing discovered vulnerabilities
- **Implementation**: ZAP baseline scan is executed against the deployed application with network-level access

### 8. Results Aggregation and Upload
- **Tool Used**: Custom Python Script + DefectDojo API
- **Purpose**: All security scan results are centralized in DefectDojo for unified vulnerability management
- **Output**: Consolidated security dashboard with all findings
- **Implementation**: Reports from all previous stages are automatically uploaded to DefectDojo instance via REST API


## Test Application

This security pipeline was validated using **OWASP Mutillidae II**, a deliberately vulnerable web application designed for security testing and training purposes.

- **Application Repository**: https://github.com/webpwnized/mutillidae
- **Results**: All security scan results and vulnerability findings demonstrated in this project were generated against the Mutillidae application


## Technical Specifications


### Security Considerations
- All sensitive credentials are managed through GitLab CI/CD variables
- API communications are secured with authentication tokens
- Report data is handled according to organizational security policies
- Container images are pulled from trusted registries only



This DevSecOps pipeline represents a comprehensive approach to automated security testing, implementing industry best practices for secure software development and establishing a foundation for continuous security improvement.