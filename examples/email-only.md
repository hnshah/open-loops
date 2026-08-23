# Example — Email only

This example tests whether Open Loops can be useful with one source while staying honest about closure scope.

## Activity

```text
Mon 09:10  You → Dana
I'll send the pricing model by Wednesday.

Tue 14:05  Vendor → You
I'll get the revised MSA back to you tomorrow.

Wed 08:20  Customer → You
Can you confirm whether SSO is included in our plan?

Wed 17:30  You → Dana
Attached is the pricing model.

Thu 11:00  Newsletter
Five trends in enterprise software...
```

## Expected result

Surface:

- waiting on the vendor if the revised MSA has not arrived after the expected time
- respond to the customer's direct SSO question if no answer exists

Suppress:

- Dana pricing model because later delivery closes it
- newsletter because it creates no obligation

## Trust note

Because only email is available, the system cannot prove that the SSO question was answered in a meeting or chat. If that possibility is material, confidence should reflect the limited resolution scope.
