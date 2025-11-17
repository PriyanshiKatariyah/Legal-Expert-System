% Cyber fraud / online crime rules

% Facts for 'user' written at runtime.

% Shared OTP indicates high fraud risk
shared_otp(Person) :-
    otp_shared(Person).

% Clicked phishing link
clicked_phishing_link(Person) :-
    clicked_link(Person, yes).

% Unauthorized transaction detected
unauthorized_transfer(Person) :-
    unauthorized_transaction(Person).

% Identity theft risk (combination)
identity_theft_risk(Person) :-
    shared_otp(Person),
    unauthorized_transfer(Person).

% Suggested action rule
file_cyber_complaint(Person) :-
    (unauthorized_transfer(Person) ; identity_theft_risk(Person)).
