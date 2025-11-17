% Traffic violations rules (medium complexity)

% Helmet missing
helmet_missing(Person) :-
    helmet(Person, no).

% License invalid or missing
license_invalid(Person) :-
    has_license(Person, no).

% Overspeeding if recorded speed > speed limit
overspeeding(Person) :-
    recorded_speed(Person, Speed),
    speed_limit(Person, Limit),
    Speed > Limit.

% Drunk driving (if breathalyzer reading > 0.03 as example)
drunk_driving(Person) :-
    breathalyzer(Person, Reading),
    Reading > 0.03.

% Seatbelt not worn
seatbelt_missing(Person) :-
    seatbelt(Person, no).

% Example composite query: Serious traffic offence
serious_traffic_offence(Person) :-
    (drunk_driving(Person) ; license_invalid(Person), overspeeding(Person)).

