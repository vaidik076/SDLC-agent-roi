"""
Domain-specific profiles for enterprise AI agents.

Each domain defines:
- Business Owner
- Skills
- Input Types
- Output Types

The metadata generator uses these profiles to create
realistic enterprise agents.
"""

DOMAIN_PROFILES = {

    "Finance": {
        "owner": "Finance Manager",

        "skills": [
            "Financial Analysis",
            "Invoice Processing",
            "Forecasting",
            "Data Validation",
            "Risk Analysis",
            "OCR",
            "Compliance Checking"
        ],

        "inputs": [
            "Invoices",
            "Excel",
            "ERP",
            "PDF",
            "CSV",
            "Email"
        ],

        "outputs": [
            "Financial Report",
            "Audit Report",
            "KPI Report",
            "Recommendation"
        ]
    },

    "Human Resources": {
        "owner": "HR Manager",

        "skills": [
            "Resume Screening",
            "Employee Onboarding",
            "Document Parsing",
            "Sentiment Analysis",
            "Policy Validation",
            "Scheduling",
            "Knowledge Retrieval"
        ],

        "inputs": [
            "Resume",
            "PDF",
            "Email",
            "HRMS",
            "Word Document"
        ],

        "outputs": [
            "Candidate Ranking",
            "Summary",
            "Recommendation",
            "Email"
        ]
    },

    "Sales": {
        "owner": "Sales Director",

        "skills": [
            "Lead Scoring",
            "Forecasting",
            "Recommendation",
            "CRM Analysis",
            "Customer Segmentation",
            "Proposal Generation"
        ],

        "inputs": [
            "CRM",
            "Email",
            "Excel",
            "Salesforce"
        ],

        "outputs": [
            "Sales Report",
            "Prediction",
            "Recommendation",
            "Dashboard"
        ]
    },

    "Marketing": {
        "owner": "Marketing Manager",

        "skills": [
            "Content Generation",
            "SEO Analysis",
            "Campaign Analysis",
            "Customer Segmentation",
            "Trend Detection",
            "Social Media Analysis"
        ],

        "inputs": [
            "Website",
            "CSV",
            "Analytics",
            "Social Media"
        ],

        "outputs": [
            "Campaign Report",
            "Dashboard",
            "Recommendation",
            "Summary"
        ]
    },

    "IT": {
        "owner": "IT Manager",

        "skills": [
            "Log Analysis",
            "Code Generation",
            "Root Cause Analysis",
            "Monitoring",
            "Automation",
            "Knowledge Retrieval"
        ],

        "inputs": [
            "Log Files",
            "Jira",
            "GitHub",
            "API"
        ],

        "outputs": [
            "Incident Report",
            "Alert",
            "Dashboard",
            "Recommendation"
        ]
    },

    "Legal": {
        "owner": "Legal Counsel",

        "skills": [
            "Contract Review",
            "Legal Research",
            "Clause Extraction",
            "Document Parsing",
            "Risk Analysis"
        ],

        "inputs": [
            "Contracts",
            "PDF",
            "Word Document"
        ],

        "outputs": [
            "Legal Report",
            "Summary",
            "Recommendation"
        ]
    }
}