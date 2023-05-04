-- Find description about the crime
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND street = "Humphrey Street"

-- Find transcripts of interviews
SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;


-- Find answers
SELECT p.name, a.city, p2.name
FROM people AS p
JOIN bank_accounts AS b ON p.id = b.person_id AND b.account_number IN (
    SELECT account_number FROM atm_transactions WHERE (
        year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street"
        AND transaction_type = "withdraw"
    )
)
JOIN bakery_security_logs AS s ON p.license_plate = s.license_plate AND (
    s.year = 2021 AND s.month = 7 AND s.day = 28 AND s.hour = 10 AND
    s.minute BETWEEN 15 AND 25 AND s.activity = "exit"
)
JOIN phone_calls AS c ON c.caller = p.phone_number AND (
    c.year = 2021 AND c.month = 7 AND c.day = 28 AND c.duration < 60
)
JOIN passengers AS ps ON p.passport_number = ps.passport_number
JOIN flights AS f ON f.id = ps.flight_id AND (
    f.year = 2021 AND f.month = 7 AND f.day = 29 AND f.hour < 12
)
JOIN airports AS a ON a.id = f.destination_airport_id
JOIN people AS p2 ON c.receiver = p2.phone_number;