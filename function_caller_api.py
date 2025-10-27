import json
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Pre-Defined Functions (for reference) ---
# These are the functions the API will map to.
# get_ticket_status(ticket_id: int)
# schedule_meeting(date: str, time: str, meeting_room: str)
# get_expense_balance(employee_id: int)
# calculate_performance_bonus(employee_id: int, current_year: int)
# report_office_issue(issue_code: int, department: str)

class FunctionCallResponse(BaseModel):
    name: str
    arguments: str

@app.get("/execute", response_model=FunctionCallResponse)
async def execute_function_call(q: str):
    # 1. Ticket Status
    ticket_match = re.match(r"What is the status of ticket (\d+)\?", q)
    if ticket_match:
        ticket_id = int(ticket_match.group(1))
        return FunctionCallResponse(
            name="get_ticket_status",
            arguments=json.dumps({"ticket_id": ticket_id})
        )

    # 2. Meeting Scheduling
    meeting_match = re.match(r"Schedule a meeting on ([\d-]+) at ([\d:]+) in (Room \w+)\.", q)
    if meeting_match:
        date, time, room = meeting_match.groups()
        return FunctionCallResponse(
            name="schedule_meeting",
            arguments=json.dumps({"date": date, "time": time, "meeting_room": room})
        )

    # 3. Expense Reimbursement
    expense_match = re.match(r"Show my expense balance for employee (\d+)\.", q)
    if expense_match:
        employee_id = int(expense_match.group(1))
        return FunctionCallResponse(
            name="get_expense_balance",
            arguments=json.dumps({"employee_id": employee_id})
        )

    # 4. Performance Bonus
    bonus_match = re.match(r"Calculate performance bonus for employee (\d+) for (\d+)\.", q)
    if bonus_match:
        employee_id = int(bonus_match.group(1))
        current_year = int(bonus_match.group(2))
        return FunctionCallResponse(
            name="calculate_performance_bonus",
            arguments=json.dumps({"employee_id": employee_id, "current_year": current_year})
        )

    # 5. Office Issue Reporting
    issue_match = re.match(r"Report office issue (\d+) for the ([\w\s]+) department\.", q)
    if issue_match:
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2)
        return FunctionCallResponse(
            name="report_office_issue",
            arguments=json.dumps({"issue_code": issue_code, "department": department})
        )

    # If no pattern matches
    raise HTTPException(status_code=400, detail="Query did not match any known function pattern.")

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
