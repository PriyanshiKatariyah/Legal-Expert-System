% Tenant-Landlord rules (knowledge + rules)

% Eviction invalid if rent is paid and notice is given
eviction_invalid(Person) :-
    rent_paid(Person),
    notice_given(Person).

% Tenant can claim refund if deposit not returned after 30 days
tenant_refund_claim(Person) :-
    deposit_not_returned(Person),
    days_since_vacate(Person, Days),
    Days > 30.

% Month-to-month tenancy if no written agreement
tenancy_month_to_month(Person) :-
    written_agreement(Person, no).

% Landlord can deduct if property damage is found
landlord_can_deduct(Person) :-
    property_damage(Person, yes).

% Eviction allowed if rent unpaid for 2+ months
eviction_allowed(Person) :-
    rent_unpaid_months(Person, Months),
    Months >= 2.

% Tenant rights for deposit
tenant_rights_deposit(Person) :-
    property_damage(Person, no),
    deposit_not_returned(Person).

