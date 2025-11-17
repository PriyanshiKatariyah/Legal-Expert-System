% Contract valid if signed by both and essential terms present
contract_valid(Person) :-
    signed_by_both(Person),
    essential_terms_present(Person).

% Breach of contract if terms broken
breach_of_contract(Person) :-
    terms_broken(Person).

% Remedy available example rule: if breach occurred and some days passed
contract_remedy(Person) :-
    breach_of_contract(Person),
    days_since_breach(Person, Days),
    Days >= 0.

