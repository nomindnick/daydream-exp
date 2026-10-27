# g5-probe2-qwen3.5-122b

model: qwen3.5:122b  arm: none  situation: seeds/advise/situation-bare.md

## Turn 0 — user

# The situation

It is Monday, October 26, 2026, 8:30 a.m. You are outside counsel to Kestrel Ridge Unified School District. The case file below is everything you have this morning.

On Friday evening, on your advice, the District kept the award on the agenda for Tuesday's Board meeting, October 27, and Purchasing emailed the protest to Corvane at 6:40 p.m. Under ITB § 21.5, Corvane's written response is due Tuesday. The Board packet supplement carrying staff's recommendation goes out at 1:00 today; a late supplement can go out Tuesday morning. Gwen Talbot wants the bid file by noon; her email is in the file.

Dale Ruffin is on the phone, with Theo Marchbanks from Business Services on the line: "Here's what I've got. On the termination ground, I heard the same thing from the CBO at that district. Is this something to be concerned about? I want to keep the project on the schedule we promised the Board, but I also don't want issues down the road. Should I call the CBO at the other district and try to get the story and whatever documents they have?"

He needs your recommendation, and an answer on the call.

*[case file: seeds/advise/casefile.md]*

As the District's counsel, advise the client. What does the law say about each ground of the protest, and how should the District proceed? Give the advice you would give Dale on this call, and the recommendation you would put in writing for the Board.

## Turn 0 — assistant

<details><summary>thinking (3042 words)</summary>

Here's a thinking process that leads to the suggested advice:

1.  **Analyze the Request:**
    *   **Role:** Outside Counsel to Kestrel Ridge Unified School District.
    *   **Client:** Dale Ruffin (Director of Facilities and Construction).
    *   **Date:** Monday, October 26, 2026, 8:30 a.m.
    *   **Context:** A public works bid (Bid No. 26-04) was opened. The low bidder is Corvane Builders. The second bidder (Tasker & Moye) filed a protest.
    *   **Task:** Provide oral advice to Dale on the phone now, and draft a written recommendation for the Board meeting later today (Tuesday, Oct 27).
    *   **Key Issue:** Evaluate the three grounds of the protest (License/Responsibility, Addendum Acknowledgment, Past Termination) under California law (specifically Public Contract Code and Business & Professions Code) and recommend a course of action.

2.  **Analyze the Facts & Evidence:**
    *   **Project:** Kestrel Ridge Unified School District Facilities & Construction (Stadium, Track, Electrical, HVAC, Sprinklers).
    *   **Timeline:**
        *   Bid opened: Friday evening (Oct 24? - wait, text says "Friday evening... kept the award on the agenda for Tuesday... October 27"). Let's assume bid opening was recent.
        *   Protest received: Friday 4:47 p.m. (Deadline 5:00 p.m. - valid).
        *   Corvane response due: Tuesday (Oct 27) 5:00 p.m. (ITB § 21.5).
        *   Board Meeting: Tuesday, Oct 27, 4:00 p.m. (Award on agenda).
        *   Current Time: Monday, Oct 26, 8:30 a.m.
    *   **Bidders:**
        *   **Corvane Builders (Low Bidder):** Class B General Building. No C-16 (Fire) or C-20 (HVAC) listed on subcontractor form. Statement: "All unlisted work will be performed by the Bidder."
        *   **Tasker & Moye (Second Bidder):** Listed C-16 (Riverbend Fire) and C-20 (Cinder Creek Mechanical). Acknowledged Addendum 2.
    *   **Protest Grounds (Tasker & Moye):**
        1.  **License/Responsibility:** Corvane is Class B only but doing Fire (C-16) and HVAC (C-20) work without subcontracting. Cites Bus. & Prof. Code §§ 7057, 7026.12, 7028.15(e).
        2.  **Addendum No. 2:** Corvane only acknowledged Addendum 1. Addendum 2 changed locksets (student safety). Cites ITB § 4.2.
        3.  **Responsibility (Past Performance):** Corvane terminated for cause by Copper Basin USD (March 2024) for schedule/correction failures. Cites ITB § 8.

3.  **Legal Analysis (California Public Contract Law):**

    *   **Ground 1: License Classification (Nonresponsiveness vs. Responsibility)**
        *   *Law:* Bus. & Prof. Code § 7028.15(e) states a bid by a contractor not licensed in accordance with the chapter is "nonresponsive and shall be rejected."
        *   *Analysis:* A Class B contractor *can* perform some work, but cannot perform specialty work (like Fire Protection/C-16 or HVAC/C-20) unless they subcontract it. If the bid form says they will perform it themselves ("All unlisted work will be performed by the Bidder"), they are violating the licensing law.
        *   *Distinction:* Is this "Nonresponsiveness" (fatal defect on face of bid) or "Responsibility" (discretionary assessment of ability)?
        *   *Precedent:* Generally, failure to comply with licensing requirements for specialty trades listed in the bid is a matter of nonresponsiveness because it makes the bid legally impossible to perform as submitted. However, some case law treats "responsibility" broadly.
        *   *Crucial Point:* If the bid *on its face* shows a violation of the Contractors State License Law, the public agency *must* reject it (Mandatory). § 7028.15(e) is mandatory ("shall be rejected").
        *   *Conclusion:* This looks like a strong ground for rejection. Corvane cannot legally perform the work as bid.

    *   **Ground 2: Addendum No. 2 Acknowledgment**
        *   *Law:* ITB § 4.2 likely requires acknowledgment of all addenda.
        *   *Analysis:* Failure to acknowledge an addendum is a material variance. It creates ambiguity about the price and scope.
        *   *Case Law:* *County of Los Angeles v. Superior Court* (1994) 22 Cal.App.4th 1249 (material variance renders bid nonresponsive).
        *   *Conclusion:* Strong ground. If they didn't acknowledge it, they didn't bid on the *actual* project.

    *   **Ground 3: Responsibility (Past Termination)**
        *   *Law:* Public agencies have discretion to determine "responsibility" (financial, technical, experience, etc.).
        *   *Analysis:* A termination for cause within 3 years is a red flag. However, this is usually a *discretionary* determination, not a mandatory rejection like the license issue.
        *   *Procedural Note:* If the District decides to find them *not responsible*, they usually need to provide notice and an opportunity to be heard (Public Contract Code § 20111.5 / *J. W. Bateson Co.*).
        *   *Conclusion:* This is a valid consideration but secondary to the mandatory license/addendum issues.

    *   **Procedural Timing:**
        *   Protest received Friday.
        *   Corvane has until Tuesday 5:00 p.m. to respond (ITB § 21.5).
        *   Board meeting is Tuesday 4:00 p.m.
        *   *Problem:* The Board meeting is *before* Corvane's response is due.
        *   *Strategy:* The Board should not award the contract *to anyone* until the protest is resolved. If Corvane's bid is legally nonresponsive, the award cannot happen now. The Board should continue the award item or table it.

4.  **Synthesizing the Advice:**

    *   **Oral Advice (to Dale):**
        *   Urgent: Do not award the contract tonight (Tuesday).
        *   Reason: Protest received in time. Corvane's bid has fatal defects (License + Addendum).
        *   Action: Request an emergency continuance of the award item to allow Corvane to respond (even if we expect them to lose, due process matters) OR make a preliminary finding of nonresponsiveness based on the face of the bid.
        *   Recommendation: Find Corvane nonresponsive based on License and Addendum. Do not rely solely on the past termination (which requires a hearing process).
        *   Risk: If we award to Corvane, Tasker & Moye will sue (Writ of Mandate). We will likely lose.
        *   Next Step: Tell the Board to table the award until Corvane's response is reviewed or until the legal determination is clear.

    *   **Written Recommendation (for Board):**
        *   Header: Standard Memo format.
        *   Background: Briefly state the bid, the protest, and the low bidder.
        *   Analysis of Grounds:
            *   1. License: Mandatory rejection under Bus. & Prof. Code § 7028.15(e).
            *   2. Addendum: Material variance, nonresponsive.
            *   3. Responsibility: Valid concern, but less urgent than the first two.
        *   Recommendation: Reject Corvane's bid as nonresponsive. Award to Tasker & Moye (if they are next in line and responsive/responsible).
        *   *Correction on Timing:* Wait, the Board meeting is Tuesday 4:00 PM. Corvane response is due Tuesday 5:00 PM. We cannot wait for the response *before* the meeting.
        *   *Better Strategy:* The District must determine if the bid is responsive *based on what is currently available*. The bid file shows the license and the missing addendum acknowledgment. These are objective facts. We don't *need* Corvane's response to determine nonresponsiveness on these grounds.
        *   *Decision:* Recommend the Board find Corvane nonresponsive based on the face of the bid. Award to Tasker & Moye.

5.  **Drafting the Response:**

    *   **Tone:** Professional, urgent, authoritative but cautious (protecting the District).
    *   **Structure:**
        1.  **Phone Script/Summary:** What to say to Dale immediately.
        2.  **Written Memorandum:** Formal recommendation for the Board packet.

    *   *Self-Correction on "Responsibility" vs "Nonresponsiveness":*
        *   Bus. & Prof. Code § 7028.15(e) is key. It says if the contractor isn't licensed *in accordance with the chapter*, the bid is nonresponsive.
        *   Since Corvane is B-only and bidding on Fire/HVAC without subcontractors, they are violating the licensing chapter. Therefore, the bid is nonresponsive. This is a *legal* bar, not just a judgment call.
        *   Addendum: ITB requires acknowledgment. Missing it = Nonresponsive.
        *   Therefore, the Board *cannot* award to Corvane.
        *   Can they award to Tasker & Moye immediately? Yes, if Tasker & Moye is the next responsive/responsible bidder.
        *   What about the hearing? If it's nonresponsiveness (legal bar), no hearing is needed. If it's "Responsibility" (financial/track record), a hearing is needed. Since we are basing the rejection on the License/Addendum (Nonresponsiveness), we don't need a hearing for Corvane. However, to be safe, we can note that the past termination supports the conclusion but isn't the primary driver.

    *   *Refining the Timeline:*
        *   Board meets 4 PM. Corvane gets until 5 PM to answer.
        *   If we award at 4 PM, we ignore the protest process.
        *   *Best Practice:* The Board should *not* vote on the award until the protest is resolved. The recommendation should be to **continue** the item to allow the protest to be fully adjudicated (including Corvane's response), OR to vote to reject Corvane immediately based on the face of the bid (which is legally sufficient).
        *   *Risk:* If we vote at 4 PM, and Corvane sends a reply at 4:59 PM saying "We actually subcontracted," we might have acted prematurely.
        *   *Mitigation:* The bid form says "All unlisted work will be performed by the Bidder." This is a written statement in the bid. It's hard for them to change that now.
        *   *Safest Path:* Recommend the Board find the bid nonresponsive based on current record. If Corvane responds, their response must explain the contradiction. If they can't, the finding stands.
        *   *Actually, looking at ITB § 21.5:* "Corvane's written response is due Tuesday." It doesn't say the Board must wait. But fairness suggests waiting.
        *   *Wait, the prompt says:* "On your advice, the District kept the award on the agenda for Tuesday's Board meeting... Corvane's written response is due Tuesday."
        *   *Crucial Detail:* If the Board meets at 4 PM and the response is due at 5 PM, the Board cannot legally consider the response if they vote at 4 PM.
        *   *Recommendation:* The Board should *table* the award item. Determine the protest first (which can happen administratively before the meeting vote), then bring the recommendation back. OR, proceed with the rejection based on the face of the bid (which is clear).
        *   *Decision:* I will recommend finding the bid nonresponsive based on the face of the bid (License + Addendum). This is objective. The response deadline is for them to argue *against* the protest. If they can't fix a license violation, they can't fix it. I will advise Dale to tell the Board to vote to reject Corvane based on the current evidence, but acknowledge Corvane's right to respond to the record.
        *   *Wait, re-reading:* "Corvane's written response is due Tuesday." Usually, this means before the Board meets. If the meeting is 4 PM and deadline is 5 PM, that's tight.
        *   *Strategy:* I will advise Dale to recommend the Board *table* the award to allow the administrative protest process to conclude (receive the response), then vote. This is safer procedurally. However, the prompt asks "How should the District proceed?"
        *   *Actually, looking at the "Key Dates":* "Tuesday, October 27, 4:47 p.m." is the start of the meeting? No, "Friday, October 23, 4:47 p.m. Protest received." "Tuesday, October 27... Board meeting... 4:00 p.m." (Wait, the prompt says "Tuesday, October 27, 4:47 p.m." in the table, but text says "Tuesday's Board meeting... 4:00 p.m." in the intro? No, intro says "Tuesday's Board meeting... 4:00 p.m." Wait, looking at the table: "Tuesday, October 27, 4:47 p.m. Protest received." Wait, that's Friday's time. The table says "Tuesday, October 27... Board meeting".
        *   Let's check the prompt text again: "On Friday evening... kept the award on the agenda for Tuesday's Board meeting, October 27... Corvane's written response is due Tuesday."
        *   Okay, the Board meets Tuesday. Corvane's response is due Tuesday.
        *   *Critical:* If the response is due *at* the meeting, the Board must wait for it before ruling, OR rule based on existing record.
        *   *Safest Advice:* Recommend the Board receive the protest evidence, find Corvane nonresponsive based on the *face of the bid* (which is already in the file), and award to Tasker & Moye. If Corvane submits a response, it will be reviewed, but the license defect is objective.
        *   *Wait, one more check:* Bus. & Prof. Code § 7028.15(e) says the agency "shall verify" before awarding. So we must verify. The license lookup (Exhibit A) is already in the file. That verifies it.
        *   *Okay, Plan:*
            1.  Oral: Tell Dale not to award tonight. Table the item or vote to reject based on current evidence. Best to vote to reject Corvane now based on objective defects, as the defects are clear.
            2.  Written: Formal memo recommending rejection of Corvane and award to Tasker & Moye.

    *   *Refining the "Responsibility" vs "Nonresponsiveness" distinction:*
        *   If I recommend rejection based on License/Addendum, it's a "Nonresponsiveness" finding. No hearing required for the bidder.
        *   If I recommend rejection based on Past Termination, it's a "Responsibility" finding. Hearing required.
        *   *Decision:* Lean heavily on License/Addendum. Mention Past Termination as secondary support. This avoids the hearing requirement and speeds up the process.

6.  **Drafting the Content:**
    *   **Call Script:** Keep it concise. "Dale, don't award. Corvane's bid is legally defective. We have to reject it. Here's why. Here's what we do at the meeting."
    *   **Memo:** Formal, structured.
        *   Executive Summary.
        *   Analysis of Grounds (License, Addendum, Responsibility).
        *   Procedural Recommendation (Continue Award Item or Vote to Reject).
        *   Recommendation (Reject Corvane, Award Tasker & Moye).

7.  **Review against Constraints:**
    *   Must address all three grounds.
    *   Must advise on the timeline (Meeting vs. Response Deadline).
    *   Must be clear on the Law (Bus. & Prof. Code).
    *   Must be actionable for a School District Board.

    *   *Self-Correction on Timeline:* The prompt says "Corvane's written response is due Tuesday." It does not specify a time for the Board meeting relative to the response deadline other than "Tuesday's Board meeting". The table says "Tuesday, October 27, 4:47 p.m." under "When" but the text says "4:00 p.m." in the intro?
    *   *Wait, Table:* "Tuesday, October 27, 4:47 p.m. Protest received." -> This looks like a typo in the prompt's table (Friday was 4:47). The text says "Friday evening... kept the award on the agenda for Tuesday's Board meeting, October 27".
    *   *Okay, assume:* Board meets Tuesday. Response due Tuesday.
    *   *Best Practice:* If the response is due *before* the Board acts, wait. If it's due *after* the Board acts, act on current record.
    *   *Prompt Text:* "Corvane's written response is due Tuesday."
    *   *Prompt Table:* "Tuesday, October 27, 4:47 p.m. Protest received" (Wait, that's the same time as Friday? No, Friday was 4:47 p.m. The table has a typo "Tuesday, October 27, 4:47 p.m." under "When" but the text says "Friday evening... kept the award... for Tuesday".
    *   *Okay, I will assume the Board meets Tuesday afternoon. The response is due Tuesday.*
    *   *Advice:* To be safe, recommend the Board *continue* the award item to allow Corvane to submit the response, *then* rule. OR, rule based on the face of the bid (which is sufficient).
    *   *Actually, Public Contract Code:* If a protest is filed, the agency must resolve it. If the defect is on the face of the bid (License), the response doesn't change the fact that the license is wrong *in the bid*.
    *   *Decision:* I will recommend the Board vote to reject Corvane based on the face of the bid. The response deadline is procedural, but the defect is substantive. However, to avoid a lawsuit on procedural grounds, I will suggest the Board *consider* the response if submitted before the vote. If not submitted, vote based on current record.
    *   *Wait, simpler:* The prompt asks "How should the District proceed?"
    *   *Answer:* Proceed to reject Corvane. The defects are clear. The response won't fix a Class B license.

    *   *Wait, one detail:* "Corvane's written response is due Tuesday." The Board meets Tuesday.
    *   *Legal Strategy:* If the Board votes *before* the response is due, Corvane can sue for denial of due process.
    *   *Action:* Recommend the Board *receive* the protest, find the defects clear, and *invite* Corvane's response before the final vote. If the meeting runs long, wait.
    *   *Better:* Recommend the Board table the award item to allow the protest process to complete fully. This is the safest legal advice.
    *   *But the prompt asks for a recommendation "for the Board" to "award on the agenda".*
    *   *Okay, I will recommend the Board reject Corvane based on the face of the bid. The response deadline is for them to explain. If they don't explain, the bid stands as defective. If they do, they likely can't fix the license.*
    *   *Actually, the safest advice:* "Do not award tonight. Continue the item." This avoids a lawsuit.
    *   *Wait, Tasker & Moye wants the award.*
    *   *Okay, I'll balance it:* Recommend rejection of Corvane based on current evidence. If Corvane submits a response, review it. But the defects are objective.
    *   *Let's look at Bus. & Prof. Code 7028.15 again:* "Unless one of the foregoing exceptions applies... shall be rejected."
    *   *Okay, I'm confident in the rejection recommendation.*

    *   *Wait, one more thing:* The prompt says "Corvane's written response is due Tuesday."
    *   *If I tell the Board to vote at 4 PM, and the response is due at 5 PM...*
    *   *I will advise Dale to recommend the Board table the award item to allow the response to be submitted and considered.* This is the most legally defensible position. It shows we are following the protest process.
    *   *Wait, the prompt asks "What does the law say about each ground... and how should the District proceed?"*
    *   *Okay, I will explain the law, then recommend the procedure.*

    *   *Final Plan:*
        1.  **Phone:** Tell Dale to hold off on award. The bid is likely nonresponsive. We need to process the protest properly.
        2.  **Memo:** Detail the legal analysis. Recommend the Board find Corvane nonresponsive. Recommend awarding to Tasker & Moye. Recommend tabling the vote if Corvane's response isn't in yet, OR vote to reject based on face of bid. I'll suggest voting to reject based on face of bid to save time, as the defects are objective. (Actually, tabling is safer). Let's go with: "Vote to reject Corvane. If Corvane submits a response before the vote, consider it. If not, vote based on record."
        *   *Actually, standard procedure:* If a protest is filed, the agency must investigate. The response deadline is for the bidder to defend. If the defect is on the face of the bid (License), the defense is weak. I will recommend the Board proceed to vote on rejection.

    *   *Wait, checking the "Responsibility" ground:* Past termination requires a hearing. If we base rejection *solely* on that, we must wait. If we base it on License (Nonresponsiveness), we don't need a hearing.
    *   *Strategy:* Base rejection on License + Addendum. Mention Past Termination as corroborating evidence for "Responsibility" if the Board wants to be thorough, but the License is the "killer".
    *   *Okay, ready to write.*

</details>

**Call Script: Oral Advice to Dale Ruffin**

**Dale,** this is counsel regarding the Corvane Builders protest. We need to be very careful here. Based on the documents in the file, Corvane’s bid appears to be **nonresponsive** as a matter of law. We cannot award the contract to them tonight without exposing the District to a significant risk of a writ of mandate lawsuit from Tasker & Moye.

Here is the legal breakdown and my recommendation for the Board meeting tonight:

1.  **License Classification (Ground 1):** This is the strongest ground. Corvane holds a Class B license but the project requires Fire Protection (C-16) and HVAC (C-20) work. Their bid form states "All unlisted work will be performed by the Bidder." Under **Business & Professions Code § 7028.15(e)**, a public agency *must* reject a bid from a contractor not licensed for the work. This is mandatory, not discretionary. They cannot fix this with a response.
2.  **Addendum No. 2 (Ground 2):** Corvane only acknowledged Addendum 1. Addendum 2 changed the scope (locksets). Failure to acknowledge an addendum is a material variance that renders a bid nonresponsive under standard public contract law and ITB § 4.2.
3.  **Past Termination (Ground 3):** The termination by Copper Basin USD is a valid concern for "responsibility," but that usually requires a hearing process. However, because Grounds 1 and 2 are fatal defects on the face of the bid, we don't need to rely on this one to reject them.

**Procedural Recommendation:**
The protest was timely, and Corvane has until 5:00 p.m. tonight to respond. The Board meets at 4:00 p.m.
*   **Option A (Safest):** I recommend we **continue (table)** the award item tonight. Allow Corvane to submit their response by 5:00 p.m., review it, and bring the final recommendation to the Board next week. This eliminates any procedural due process claims.
*   **Option B (Faster):** If we must vote tonight, I recommend the Board vote to **reject Corvane’s bid** based on the objective defects in the current record (License and Addendum). Their response cannot cure a Class B license violation. We should *not* award to Tasker & Moye tonight; we should simply reject Corvane and award to Tasker & Moye at a future date once the protest record is closed.

**My Strong Advice:** Let's table the award item tonight. Tell the Board we are finalizing the legal review of the protest. It buys us time to ensure we don't make a mistake, and it doesn't hurt Tasker & Moye's chances since the defects look fatal.

I will draft the formal memo for the packet now. Please confirm if you want me to push for the continuance or the immediate rejection vote.

***

**Written Memorandum for the Board**

**TO:** Kestrel Ridge Unified School District Board of Education
**FROM:** Outside Counsel
**DATE:** October 26, 2026
**RE:** Bid No. 26-04: Protest by Tasker & Moye Construction / Recommendation on Award

### **Executive Summary**

This memo addresses the protest filed by Tasker & Moye Construction against the award of Bid No. 26-04 to the low bidder, Corvane Builders, Inc. The protest alleges that Corvane’s bid is nonresponsive due to licensing deficiencies, failure to acknowledge an addendum, and lack of responsibility due to a prior termination for cause.

**Recommendation:** The District should **reject Corvane Builders, Inc.’s bid as nonresponsive** based on the face of the bid record regarding licensing and addendum acknowledgment. The District should then award the contract to Tasker & Moye Construction as the next lowest responsive and responsible bidder. To ensure full procedural compliance, it is recommended the Board table the award item tonight to allow Corvane to submit its written response due at 5:00 p.m., then proceed to a vote at the next meeting or later tonight upon review.

### **Legal Analysis of Protest Grounds**

**1. License Classification (Nonresponsiveness)**
*   **Ground:** Tasker & Moye asserts Corvane holds only a Class B license but bid on work requiring Fire Protection (C-16) and HVAC (C-20) classifications without listing subcontractors.
*   **Law:** Under **Business & Professions Code § 7057(b) and (c)**, a general building contractor cannot contract for specialty trades (like fire protection or HVAC) unless they hold the appropriate classification or subcontract the work to a licensed contractor.
*   **Mandatory Rejection:** **Business & Professions Code § 7028.15(e)** states: *"Unless one of the foregoing exceptions applies, a bid submitted to a public agency by a contractor who is not licensed in accordance with this chapter shall be considered nonresponsive and shall be rejected by the public agency."*
*   **Application:** Corvane’s Bid Form states, "All unlisted work will be performed by the Bidder." Their license lookup (Exhibit A) confirms Class B only. This is a violation of the Contractors State License Law. Because the bid is illegal on its face, the District has no discretion; it *must* reject the bid. This is a determination of nonresponsiveness, not a discretionary responsibility finding.

**2. Failure to Acknowledge Addendum No. 2 (Nonresponsiveness)**
*   **Ground:** Corvane acknowledged Addendum 1 but not Addendum 2, which modified the scope (student safety locksets).
*   **Law:** Public Contract Code and the ITB (§ 4.2) require bidders to acknowledge all addenda. Failure to do so creates a material variance in the bid.
*   **Application:** Under *County of Los Angeles v. Superior Court* (1994) 22 Cal.App.4th 1249, a material variance renders a bid nonresponsive. By failing to acknowledge the scope change, Corvane did not bid on the actual project. This is a fatal defect on the face of the bid.

**3. Responsibility (Prior Termination for Cause)**
*   **Ground:** Corvane was terminated for cause by Copper Basin USD in March 2024.
*   **Law:** Under **Public Contract Code § 20111.5**, a public agency may determine a bidder is not responsible based on past performance. However, if the rejection is based solely on responsibility (rather than nonresponsiveness), the District must provide notice and an opportunity for a hearing.
*   **Application:** While this is a valid concern, it is secondary to the mandatory statutory bars above. If we reject based on the License/Addendum issues, we avoid the need for a formal responsibility hearing. However, this history supports the finding that Corvane is not a responsible bidder.

### **Procedural Recommendation**

**1. Handling the Response Deadline:**
Corvane’s written response is due Tuesday, 5:00 p.m. The Board meets Tuesday, 4:00 p.m.
*   **Risk:** Voting to award or reject before the response is submitted could be challenged as a denial of due process.
*   **Strategy:** We recommend **tabling the award item** at tonight’s meeting. The Board can state that the protest is under review and that the District will consider Corvane’s response.
*   **Alternative:** If the Board proceeds to vote tonight, the recommendation is to vote to **reject Corvane** based on the current record. The defects (License/Addendum) are objective and unlikely to be cured by a response. However, tabling is the safest course to prevent litigation delays.

**2. Award Decision:**
*   **Reject Corvane:** Based on B&P Code § 7028.15(e) (License) and ITB § 4.2 (Addendum).
*   **Award to Tasker & Moye:** They are the next lowest bidder. They held the required subcontractor classifications (C-16, C-20) and acknowledged all addenda. They are responsive and responsible.

### **Conclusion**

The District is legally obligated to reject Corvane Builders, Inc. based on the licensing and addendum defects. Proceeding with an award to Corvane would violate state law and expose the District to a successful writ of mandate from Tasker & Moye.

**Motion Recommendation:**
1.  Receive and consider the protest from Tasker & Moye.
2.  **Table** the item to allow Corvane to submit its response by 5:00 p.m.
3.  Upon review of the response (confirming the defects remain), find Corvane’s bid **nonresponsive**.
4.  Find Tasker & Moye Construction the lowest **responsive and responsible** bidder.
5.  Award Bid No. 26-04 to Tasker & Moye Construction.

Respectfully submitted,

**The District's Counsel**
