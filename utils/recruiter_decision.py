
def recruiter_decision(score):

    if score >= 90:
        return "🌟 Strong Hire"

    elif score >= 80:
        return "✅ Hire"

    elif score >= 70:
        return "⚠ Consider"

    else:
        return "❌ Reject"