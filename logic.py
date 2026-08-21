# ---------------- ANALYSIS FUNCTION ----------------
def analyze_answer(answer, question, keywords):
    score = 0
    feedback = []

    words = answer.split()

    # Length check
    if len(words) < 10:
        feedback.append("Answer is too short. Try to elaborate.")
    elif len(words) > 20:
        feedback.append("Good detailed answer.")
        score += 2
    else:
        feedback.append("Decent length.")
        score += 1

    # Keyword check
    matched = 0
    for word in keywords.get(question, []):
        if word in answer.lower():
            matched += 1

    if matched >= 2:
        feedback.append("Good use of relevant keywords.")
        score += 2
    elif matched == 1:
        feedback.append("Try adding more relevant points.")
        score += 1
    else:
        feedback.append("Answer lacks important keywords.")

    # Positive tone
    positive_words = ["confident", "achieved", "success", "improved"]

    for word in positive_words:
        if word in answer.lower():
            feedback.append("Positive tone detected.")
            score += 1
            break

    # Final verdict
    if score >= 4:
        feedback.append("Overall: Excellent answer!")
    elif score >= 2:
        feedback.append("Overall: Good, but can improve.")
    else:
        feedback.append("Overall: Needs improvement.")

    return min(score, 5), feedback