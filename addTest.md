## Add a test event for tomorrow
```sh
TOMORROW=$(date -d "+1 day" +%Y-%m-%d 2>/dev/null || date -v+1d +%Y-%m-%d)

aws lambda invoke \
--function-name ManageDepartureEvents \
--payload "{
\"action\": \"add\",
\"country\": \"TestCountry\",
\"departureDate\": \"$TOMORROW\",
\"purpose\": \"Test\",
\"notes\": \"This is a test notification\"
}" \
response.json
```
## Manually Trigger Check (to test immediately)

```sh
aws lambda invoke \
--function-name DepartureNotificationChecker \
--payload '{}' \
response.json
```







