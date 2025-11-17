import os

# -----------------------------------------
# Configure SWI-Prolog Environment
# -----------------------------------------
os.environ["SWI_HOME_DIR"] = r"C:\SWI-Prolog"
os.environ["PATH"] += os.pathsep + r"C:\SWI-Prolog\bin"

from flask import Flask, render_template, request, redirect, url_for
from pyswip import Prolog

app = Flask(__name__)

# -----------------------------------------
# Paths
# -----------------------------------------
PROLOG_DIR = os.path.join(os.path.dirname(__file__), "prolog")
FACTS_FILE = os.path.join(PROLOG_DIR, "facts_temp.pl")

# -----------------------------------------
# Domains (Shown on Homepage)
# -----------------------------------------
DOMAINS = {
    "tenant": "Tenant–Landlord Disputes",
    "consumer": "Consumer Rights",
    "contract": "Contract Disputes",
    "traffic": "Traffic Violations",
    "cyber": "Cyber Fraud / Online Crime",
    "employment": "Employment / Workplace Issues"
}

# -----------------------------------------
# DOMAIN CONFIG (Queries + Advice + Rule Files)
# -----------------------------------------
DOMAIN_CONFIG = {
    "tenant": {
        "queries": [
            ("Eviction Invalid", "eviction_invalid(user)"),
            ("Refund Claim", "tenant_refund_claim(user)"),
            ("Month-to-Month Tenancy", "tenancy_month_to_month(user)"),
            ("Landlord Deduction Allowed", "landlord_can_deduct(user)"),
            ("Eviction Allowed", "eviction_allowed(user)"),
            ("Deposit Rights", "tenant_rights_deposit(user)")
        ],
        "advice": {
            "Eviction Invalid": "Eviction cannot proceed because the tenant has fulfilled essential obligations such as paying rent and giving proper notice. The landlord is advised to resolve the matter amicably or seek mediation.",
            "Refund Claim": "Since the deposit has not been returned within the statutory period, the tenant may request a refund in writing or escalate to rent authorities.",
            "Month-to-Month Tenancy": "No written agreement means tenancy operates month-to-month. Both parties should consider formalizing the agreement to avoid disputes.",
            "Landlord Deduction Allowed": "Deductions from the security deposit are allowed only when actual damage exists. A written deduction statement is recommended.",
            "Eviction Allowed": "Eviction is permissible because rent remains unpaid for an extended period. The landlord may issue formal notice while the tenant should clear dues or negotiate.",
            "Deposit Rights": "Tenant is entitled to full refund since no damage exists and dues are clear. A written refund request is recommended."
        },
        "next_steps": {
            "Eviction Invalid": {
                "yes": [
                    "Attempt an amicable resolution with landlord (record discussions).",
                    "If rejected, consider mediation or a written request through a legal aid clinic."
                ],
                "no": [
                    "Verify rent receipts and notice records; gather documentary proof.",
                    "If doubt persists, consult legal aid or landlord association."
                ]
            },
            "Refund Claim": {
                "yes": [
                    "Send a formal written refund request to the landlord.",
                    "If ignored, file a complaint with the rent authority."
                ],
                "no": [
                    "Request deposit breakdown and verify deductions.",
                    "Gather photo evidence of the property condition."
                ]
            },
            "Month-to-Month Tenancy": {
                "yes": [
                    "Consider signing a formal written agreement.",
                    "Keep written proof of all payments."
                ],
                "no": [
                    "Store original agreement safely for future reference."
                ]
            },
            "Landlord Deduction Allowed": {
                "yes": [
                    "Request itemized deduction summary.",
                    "Seek mediation if deductions feel excessive."
                ],
                "no": [
                    "Demand full deposit refund with written request."
                ]
            },
            "Eviction Allowed": {
                "yes": [
                    "Clear dues immediately or negotiate repayment.",
                    "Seek legal advice to halt eviction."
                ],
                "no": [
                    "Maintain proof of all payments and notices."
                ]
            },
            "Deposit Rights": {
                "yes": [
                    "Send written refund request.",
                    "File complaint if deposit is withheld."
                ],
                "no": [
                    "Request deduction breakdown from landlord."
                ]
            }
        },
        "rule_file": os.path.join(PROLOG_DIR, "tenant_rules.pl")
    },

    "consumer": {
        "queries": [
            ("Refund Allowed", "refund_allowed(user)"),
            ("Replacement Allowed", "replacement_allowed(user)"),
            ("Complaint Possible", "consumer_complaint_possible(user)")
        ],
        "advice": {
            "Refund Allowed": "Product defect qualifies for refund. Contact seller with receipt.",
            "Replacement Allowed": "Defect covered under policy. Request replacement.",
            "Complaint Possible": "Seller is uncooperative. File consumer complaint."
        },
        "next_steps": {
            "Refund Allowed": {
                "yes": [
                    "Request refund with bill copy.",
                    "Escalate to grievance cell if refused."
                ],
                "no": [
                    "Check warranty or repair policies."
                ]
            },
            "Replacement Allowed": {
                "yes": [
                    "Request replacement formally.",
                    "Escalate if delayed."
                ],
                "no": [
                    "Document defect and check warranty terms."
                ]
            },
            "Complaint Possible": {
                "yes": [
                    "File complaint with evidence.",
                    "Attach bill and product proof."
                ],
                "no": [
                    "Try negotiating with seller."
                ]
            }
        },
        "rule_file": os.path.join(PROLOG_DIR, "consumer_rules.pl")
    },

    "contract": {
        "queries": [
            ("Contract Valid", "contract_valid(user)"),
            ("Breach of Contract", "breach_of_contract(user)"),
            ("Remedy Available", "contract_remedy(user)")
        ],
        "advice": {
            "Contract Valid": "Contract contains essential terms and is valid.",
            "Breach of Contract": "A term was violated. Issue notice.",
            "Remedy Available": "Remedies include compensation or mediation."
        },
        "next_steps": {
            "Contract Valid": {
                "yes": [
                    "Store signed contract safely.",
                    "Record all communication."
                ],
                "no": [
                    "Clarify missing terms."
                ]
            },
            "Breach of Contract": {
                "yes": [
                    "Send legal notice.",
                    "Gather evidence before action."
                ],
                "no": [
                    "Recheck contract terms."
                ]
            },
            "Remedy Available": {
                "yes": [
                    "Seek compensation or mediation."
                ],
                "no": [
                    "Attempt renegotiation."
                ]
            }
        },
        "rule_file": os.path.join(PROLOG_DIR, "contract_rules.pl")
    },

    "traffic": {
        "queries": [
            ("Helmet Missing", "helmet_missing(user)"),
            ("License Invalid", "license_invalid(user)"),
            ("Overspeeding", "overspeeding(user)"),
            ("Drunk Driving", "drunk_driving(user)"),
            ("Seatbelt Missing", "seatbelt_missing(user)"),
            ("Serious Traffic Offence", "serious_traffic_offence(user)")
        ],
        "advice": {
            "Helmet Missing": "Helmet mandatory; wearing avoids penalties.",
            "License Invalid": "Driving without license is serious offence.",
            "Overspeeding": "Follow posted speed limits.",
            "Drunk Driving": "Major offence; do not drive.",
            "Seatbelt Missing": "Seatbelt is mandatory.",
            "Serious Traffic Offence": "Multiple violations detected."
        },
        "next_steps": {
            "Helmet Missing": {"yes": ["Wear helmet."], "no": ["Continue following safety rules."]},
            "License Invalid": {"yes": ["Renew license."], "no": ["Keep license available."]},
            "Overspeeding": {"yes": ["Pay fine."], "no": ["Maintain safe speed."]},
            "Drunk Driving": {"yes": ["Seek legal help."], "no": ["Drive responsibly."]},
            "Seatbelt Missing": {"yes": ["Wear seatbelt."], "no": ["Continue compliance."]},
            "Serious Traffic Offence": {"yes": ["Consult traffic lawyer."], "no": ["Avoid violations."]}
        },
        "rule_file": os.path.join(PROLOG_DIR, "traffic_rules.pl")
    },

    "cyber": {
        "queries": [
            ("OTP Shared", "shared_otp(user)"),
            ("Clicked Phishing Link", "clicked_phishing_link(user)"),
            ("Unauthorized Transfer", "unauthorized_transfer(user)"),
            ("Identity Theft Risk", "identity_theft_risk(user)"),
            ("File Cyber Complaint", "file_cyber_complaint(user)")
        ],
        "advice": {
            "OTP Shared": "OTP sharing exposes you to fraud.",
            "Clicked Phishing Link": "Reset passwords and scan device.",
            "Unauthorized Transfer": "Report immediately and block account.",
            "Identity Theft Risk": "Identity theft likely; take action.",
            "File Cyber Complaint": "File cyber complaint with evidence."
        },
        "next_steps": {
            "OTP Shared": {"yes": ["Change passwords immediately."], "no": ["Maintain hygiene."]},
            "Clicked Phishing Link": {"yes": ["Scan device; reset credentials."], "no": ["Avoid unknown links."]},
            "Unauthorized Transfer": {"yes": ["Freeze account; file report."], "no": ["Monitor activity."]},
            "Identity Theft Risk": {"yes": ["File complaint; freeze cards."], "no": ["Maintain cyber safety."]},
            "File Cyber Complaint": {"yes": ["Submit evidence to cyber cell."], "no": ["Monitor accounts."]}
        },
        "rule_file": os.path.join(PROLOG_DIR, "cyber_rules.pl")
    },

    "employment": {
        "queries": [
            ("Salary Due", "salary_due(user)"),
            ("Wrongful Termination", "wrongful_termination(user)"),
            ("Harassment Reported", "harassment_reported(user)"),
            ("Remedy Available", "employment_remedy(user)")
        ],
        "advice": {
            "Salary Due": "Unpaid salary is a major labour violation.",
            "Wrongful Termination": "Termination without notice may be wrongful.",
            "Harassment Reported": "Document and report to HR/legal cell.",
            "Remedy Available": "Compensation or reinstatement possible."
        },
        "next_steps": {
            "Salary Due": {"yes": ["Collect proof; file complaint."], "no": ["Ask employer for clarification."]},
            "Wrongful Termination": {"yes": ["Send grievance notice."], "no": ["Check contract clauses."]},
            "Harassment Reported": {"yes": ["Document & report."], "no": ["Follow HR procedures."]},
            "Remedy Available": {"yes": ["Seek mediation/legal help."], "no": ["Try negotiation."]}
        },
        "rule_file": os.path.join(PROLOG_DIR, "employment_rules.pl")
    }
}

# ---------------------------------------------------
# WRITE FACTS FOR EACH DOMAIN
# ---------------------------------------------------
def write_facts(domain, form):
    lines = []

    # ---------- TENANT ----------
    if domain == "tenant":
        if form.get("rent_paid") == "Yes":
            lines.append("rent_paid(user).")
        if form.get("notice_given") == "Yes":
            lines.append("notice_given(user).")
        if form.get("deposit_returned") == "No":
            lines.append("deposit_not_returned(user).")
        lines.append(f"days_since_vacate(user, {int(form.get('days_since') or 0)}).")
        lines.append(f"property_damage(user, {form.get('damage','no')}).")
        lines.append(f"rent_unpaid_months(user, {int(form.get('rent_unpaid') or 0)}).")
        lines.append(f"written_agreement(user, {form.get('written_agreement','no')}).")

    # ---------- CONSUMER ----------
    elif domain == "consumer":
        if form.get("defective") == "Yes":
            lines.append("product_defective(user).")
        lines.append(f"days_since_purchase(user, {int(form.get('days_since_purchase') or 0)}).")
        if form.get("bill_present") == "Yes":
            lines.append("bill_present(user).")
        if form.get("warranty") == "Yes":
            lines.append("warranty_active(user).")

    # ---------- CONTRACT ----------
    elif domain == "contract":
        if form.get("signed_by_both") == "Yes":
            lines.append("signed_by_both(user).")
        if form.get("essential_terms") == "Yes":
            lines.append("essential_terms_present(user).")
        if form.get("terms_broken") == "Yes":
            lines.append("terms_broken(user).")
        lines.append(f"days_since_breach(user, {int(form.get('days_since_breach') or 0)}).")

    # ---------- TRAFFIC ----------
    elif domain == "traffic":
        lines.append(f"helmet(user, {form.get('helmet','yes')}).")
        has_license = "yes" if form.get("license") == "Yes" else "no"
        lines.append(f"has_license(user, {has_license}).")
        lines.append(f"recorded_speed(user, {int(form.get('recorded_speed') or 0)}).")
        lines.append(f"speed_limit(user, {int(form.get('speed_limit') or 0)}).")
        lines.append(f"breathalyzer(user, {float(form.get('breathalyzer') or 0.0)}).")
        lines.append(f"seatbelt(user, {form.get('seatbelt','yes')}).")

    # ---------- CYBER ----------
    elif domain == "cyber":
        if form.get("otp_shared") == "Yes":
            lines.append("otp_shared(user).")
        if form.get("clicked_link") == "Yes":
            lines.append("clicked_link(user, yes).")
        else:
            lines.append("clicked_link(user, no).")
        if form.get("unauthorized_transaction") == "Yes":
            lines.append("unauthorized_transaction(user).")

    # ---------- EMPLOYMENT ----------
    elif domain == "employment":
        lines.append(f"unpaid_salary_months(user, {int(form.get('unpaid_salary_months') or 0)}).")
        tw = "yes" if form.get("terminated_without_notice") == "Yes" else "no"
        lines.append(f"terminated_without_notice(user, {tw}).")
        hr = "yes" if form.get("harassment") == "Yes" else "no"
        lines.append(f"harassment(user, {hr}).")

    # Write to Prolog file
    with open(FACTS_FILE, "w") as f:
        for ln in lines:
            f.write(ln + "\n")


# ---------------------------------------------------
# ROUTES
# ---------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", domains=DOMAINS)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/form/<domain>")
def form_page(domain):
    if domain not in DOMAINS:
        return redirect(url_for("index"))
    return render_template("case_form.html", domain=domain, domain_name=DOMAINS[domain])

@app.route("/analyze", methods=["POST"])
def analyze():
    print("DOMAIN RECEIVED:", request.form)   # DEBUG
    
    domain = request.form.get("domain")

    if not domain or domain not in DOMAINS:
        return redirect(url_for("index"))

    # Write temporary facts
    write_facts(domain, request.form)

    try:
        prolog = Prolog()
        prolog.consult(DOMAIN_CONFIG[domain]["rule_file"])
        prolog.consult(FACTS_FILE)
    except Exception as e:
        print("PROLOG LOAD ERROR:", e)
        return render_template("result.html", domain_name="Error", results=[])

    results = []

    for title, q in DOMAIN_CONFIG[domain]["queries"]:
        try:
            truth = bool(list(prolog.query(q)))
        except Exception as e:
            print("QUERY ERROR:", q, e)
            truth = False

        advice = DOMAIN_CONFIG[domain]["advice"].get(title, "")

        steps_map = DOMAIN_CONFIG[domain]["next_steps"].get(title, {})
        next_steps = steps_map.get("yes" if truth else "no", [])

        results.append({
            "title": title,
            "result": "YES" if truth else "NO",
            "advice": advice if truth else "Conditions for this legal action are not satisfied.",
            "next_steps": next_steps
        })

    return render_template("result.html", domain_name=DOMAINS[domain], results=results)


# ---------------------------------------------------
# RUN
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
