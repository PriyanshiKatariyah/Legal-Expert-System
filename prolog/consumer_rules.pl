% Refund allowed if the product is defective within 10 days
refund_allowed(Person) :-
    product_defective(Person),
    days_since_purchase(Person, Days),
    Days =< 10.

% Replacement allowed if defective AND:
% - warranty is active
% OR
% - purchased within 30 days
replacement_allowed(Person) :-
    product_defective(Person),
    (   warranty_active(Person)
    ;   ( days_since_purchase(Person, Days), Days =< 30 )
    ).

% Complaint possible if:
% - product is defective
% OR
% - bill is missing
% OR
% - seller refused remedy (optional future rule)
consumer_complaint_possible(Person) :-
    product_defective(Person).

consumer_complaint_possible(Person) :-
    \+ bill_present(Person).   % no bill → complaint still possible

