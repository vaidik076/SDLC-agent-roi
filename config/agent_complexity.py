"""
Agent Complexity Configuration

This module defines:

1. Complexity profiles
   - Cost ranges
   - Operating cost
   - Hours saved
   - Automation %

2. Default complexity by business domain

3. Agent-specific overrides
"""

# ==========================================================
# Complexity Profiles
# ==========================================================

COMPLEXITY_PROFILES = {

    "LOW": {

        "implementation_cost": (50000, 90000),
        "annual_operating_cost": (10000, 20000),
        "estimated_hours_saved": (2200, 3500),
        "automation_percentage": (85, 95),

    },

    "MEDIUM": {

        "implementation_cost": (90000, 180000),
        "annual_operating_cost": (20000, 45000),
        "estimated_hours_saved": (1600, 3000),
        "automation_percentage": (70, 85),

    },

    "HIGH": {

        "implementation_cost": (180000, 300000),
        "annual_operating_cost": (45000, 80000),
        "estimated_hours_saved": (2500, 4000),
        "automation_percentage": (55, 75),

    },

}


# ==========================================================
# Default Complexity Per Business Domain
# ==========================================================

DOMAIN_COMPLEXITY = {

    "Finance": "MEDIUM",
    "Human Resources": "LOW",
    "Sales": "MEDIUM",
    "Marketing": "LOW",
    "IT": "HIGH",
    "Legal": "HIGH",
    "Healthcare": "HIGH",
    "Manufacturing": "MEDIUM",
    "Supply Chain": "MEDIUM",
    "Customer Support": "LOW",
    "Procurement": "MEDIUM",
    "Banking": "HIGH",
    "Insurance": "HIGH",
    "Retail": "LOW",
    "Education": "LOW",
    "Cybersecurity": "HIGH",
    "Telecommunications": "MEDIUM",
    "Energy": "HIGH",
    "Data & Analytics": "HIGH",
    "Operations": "MEDIUM",

}


# ==========================================================
# Agent-Specific Overrides
# (Only agents that differ from their domain default)
# ==========================================================

AGENT_COMPLEXITY_OVERRIDE = {

    # -----------------------
    # Finance
    # -----------------------

    "Invoice Processing Agent": "LOW",
    "Expense Validation Agent": "LOW",
    "Audit Assistant": "HIGH",
    "Financial Planning Agent": "HIGH",

    # -----------------------
    # Human Resources
    # -----------------------

    "Resume Screening Agent": "MEDIUM",
    "Employee Onboarding Agent": "LOW",
    "Attrition Prediction Agent": "HIGH",

    # -----------------------
    # Sales
    # -----------------------

    "Lead Qualification Agent": "LOW",
    "Pricing Optimization Agent": "HIGH",

    # -----------------------
    # Marketing
    # -----------------------

    "Content Generation Agent": "LOW",
    "Brand Intelligence Agent": "HIGH",

    # -----------------------
    # IT
    # -----------------------

    "IT Helpdesk Agent": "LOW",
    "Code Review Agent": "HIGH",
    "Incident Response Agent": "HIGH",

    # -----------------------
    # Legal
    # -----------------------

    "Contract Review Agent": "HIGH",
    "Legal Research Agent": "HIGH",

    # -----------------------
    # Banking
    # -----------------------

    "Fraud Detection Agent": "HIGH",
    "Credit Risk Assessment Agent": "HIGH",

    # -----------------------
    # Cybersecurity
    # -----------------------

    "Threat Detection Agent": "HIGH",
    "Security Monitoring Agent": "HIGH",

}