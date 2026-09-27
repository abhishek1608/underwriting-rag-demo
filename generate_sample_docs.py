"""
Generates 3 real PDF files standing in for the documents your production
FAISS index actually indexes: underwriting policy manual, product
guidelines, and an RCU field-investigation report. Content is written to
deliberately cover DIFFERENT topics so retrieval quality is demonstrable —
a query about "agent persistency" should NOT retrieve the medical-loading
clause, etc.
"""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os

os.makedirs("docs", exist_ok=True)
styles = getSampleStyleSheet()


def make_pdf(filename, title, paragraphs):
    doc = SimpleDocTemplate(f"docs/{filename}", pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]
    for p in paragraphs:
        story.append(Paragraph(p, styles["BodyText"]))
        story.append(Spacer(1, 10))
    doc.build(story)
    print(f"  wrote docs/{filename}  ({len(paragraphs)} paragraphs)")


make_pdf(
    "underwriting_policy_manual.pdf",
    "Underwriting Policy Manual — Section 4",
    [
        "Clause 4.1: Every proposal is scored by the early-claim prediction model at the proposal stage, before issuance. "
        "A risk band of A or B triggers mandatory referral to the RCU field-investigation team; underwriter discretion "
        "does not apply to this trigger.",

        "Clause 4.2: Claims filed within three years of policy inception fall inside the early-claim window and require "
        "RCU field verification before any payout is authorised. This applies regardless of the sum assured or the "
        "declared cause.",

        "Clause 4.3: A proposal filed within one year of inception is subject to the contestability period under the "
        "Insurance Act. Any material misstatement discovered in this window is grounds for the policy to be voided, "
        "and the claim is rejected outright rather than referred for scoring.",

        "Clause 4.4: Underwriters must record a confidence level of HIGH, MEDIUM, or LOW against every risk-factor "
        "assessment, and the final acceptance or rejection decision always rests with the underwriter, not with the "
        "model or any automated support tool.",
    ],
)

make_pdf(
    "product_guidelines.pdf",
    "Product Underwriting Guidelines — Term Life",
    [
        "Guideline 7.1: Where the claim amount exceeds 80 percent of the sum assured, a secondary medical review is "
        "mandatory before the claim can be closed, irrespective of the risk band assigned at proposal stage.",

        "Guideline 7.2: The sum-assured-to-income ratio should not ordinarily exceed 10 to 12 times annual declared "
        "income. A ratio materially above this range is treated as an insurable-interest concern and should be "
        "flagged for income verification.",

        "Guideline 7.3: Absence of any medical loading at entry ages above 55 is atypical and should prompt a review "
        "of the medical questionnaire responses for possible non-disclosure, rather than being treated as a clean "
        "profile by default.",

        "Guideline 7.4: Body Mass Index readings at medical examination above 30 fall into an elevated mortality-risk "
        "category and may attract a medical loading on premium, subject to the medical underwriter's review.",
    ],
)

make_pdf(
    "rcu_report_template.pdf",
    "RCU Field Investigation — Reporting Standards",
    [
        "Section A — Income Verification: The field officer must corroborate declared income against bank statement "
        "credits or GST filings where the applicant is self-employed. A variance greater than 15 percent between "
        "declared and verified income should be reported as an adverse income finding.",

        "Section B — Agent Conduct Review: Investigators must check the sourcing agent's prior case history. An agent "
        "with more than one prior Null and Void outcome, or a persistency rate materially below the branch average, "
        "should be flagged to the Agency Compliance team as a systemic risk indicator independent of the individual case.",

        "Section C — Health Disclosure: Field observations on health are indicative only. Any suspected non-disclosure "
        "must be referred for a formal Attending Physician Statement; field investigators are not authorised to draw "
        "a medical conclusion, and the final medical view must rest on declared history and medical records.",

        "Section D — Reinsurer Submission: Cases with an adverse RCU finding must be uploaded to the reinsurer portal "
        "with all supporting documents before the underwriter's final decision is recorded, so that reinsurance cover "
        "eligibility is established in parallel with the underwriting decision.",
    ],
)

print("Done.")
