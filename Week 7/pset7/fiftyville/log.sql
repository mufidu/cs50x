-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Read all the crimes reports
SELECT * FROM crime_scene_reports;

-- We got desciption: Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

-- read the interviews with witnessess
SELECT * from interviews
WHERE month = 7 AND day = 28 AND year = 2020;


-- Read courthouse logs
SELECT license_plate from courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit";

-- Get Eugene's license plat (47592FJ)
SELECT license_plate FROM people WHERE name = "Eugene";

-- When Eugene comes to the courthouse
SELECT * FROM courthouse_security_logs WHERE license_plate = '47592FJ';

-- Read calls activities logs
SELECT caller, receiver, duration FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;

-- Find the flight
SELECT flights.id FROM flights
JOIN airports ON origin_airport_id = airports.id
WHERE airports.city = "Fiftyville" AND flights.year = 2020 AND flights.month = 7 AND flights.day = 29
ORDER BY flights.hour LIMIT 1;

-- find who withdrew that day and flew tomorrow morning and made a call that day (only FOUND Ernest)
SELECT DISTINCT(name) FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.day = 28 AND atm_transactions.year = 2020 AND atm_transactions.month = 7 AND people.name IN (
SELECT name from PEOPLE
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON origin_airport_id = airports.id
WHERE flights.id = 36) AND people.license_plate IN (
SELECT license_plate from courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit") AND people.phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60);

-- find who Ernest called with (FOUND BERTHOLD)
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.caller = (SELECT phone_number FROM people WHERE name = "Ernest") AND phone_calls.year = 2020 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration < 60;

-- find where did Ernest fly to (FOUND LONDON)
SELECT city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.id = 36;
