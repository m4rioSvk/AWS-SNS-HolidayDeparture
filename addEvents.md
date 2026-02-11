## Here we can add as many events as we need

aws lambda invoke \
--function-name ManageDepartureEvents \
--cli-binary-format raw-in-base64-out \
--payload '{
"action": "add",
"country": "Europe",
"departureDate": "2026-03-11",
"purpose": "Moving-out",
"notes": "Remember passport and have a safe trip!"
}' \
response.json

## Delete events(need to check for the event ID first)

aws lambda invoke \
--function-name ManageDepartureEvents \
--cli-binary-format raw-in-base64-out \
--payload '{
"action": "delete",
"eventId": "ea186002-da0c-4a6a-b20b-bdf07837b8c9"
}' \
response.json

## Check all the events

aws lambda invoke \
  --function-name ManageDepartureEvents \
  --cli-binary-format raw-in-base64-out \
  --payload '{"action": "list"}' \
  response.json

## Event data structure in json format 

{
  "eventId": "uuid-generated-automatically",
  "country": "Japan",
  "departureDate": "2026-03-15",
  "returnDate": "2026-03-25",
  "purpose": "Vacation",
  "notes": "Remember passport and visa",
  "createdAt": "2026-02-11T10:30:00"
}
