% Salary due >= 2 months
salary_due(Person) :-
    unpaid_salary_months(Person, Months),
    Months >= 2.

% Wrongful termination if terminated_without_notice yes and no valid reason
wrongful_termination(Person) :-
    terminated_without_notice(Person, yes).

% Harassment reported
harassment_reported(Person) :-
    harassment(Person, yes).

% Remedy available — if salary due or wrongful termination or harassment
employment_remedy(Person) :-
    salary_due(Person);
    wrongful_termination(Person);
    harassment_reported(Person).

