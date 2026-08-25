# Use-Case Flow Specification — Inter-City Freight Load Matching Marketplace

## Use Case: Submit Bid on Freight Load

**Primary Actor:** Freight Carrier
**Related Use Cases:** Includes «include» Verify Carrier Permits

---

### Preconditions
1. The Freight Carrier is registered and logged into the system.
2. The Freight Carrier's account has valid, non-expired permits and licensing documents on file.
3. At least one freight load posted by a Shipper is currently open for bidding (status: "Bidding").
4. The auction timeframe for the target load has not yet closed.

---

### Postconditions
1. The carrier's bid (amount, proposed pickup/delivery timeline) is recorded and linked to the load listing.
2. The Shipper is notified in real time that a new bid has been received.
3. The load's bid count and current best offer are updated and visible to all eligible carriers.
4. The bid remains active until the shipper awards the load or the auction window closes.

---

### Main Success Scenario
1. The Freight Carrier navigates to an open freight load listing.
2. The Carrier selects "Submit Bid" and enters a bid amount and proposed delivery timeline.
3. The system triggers the included use case **Verify Carrier Permits**, confirming the carrier's permits and licenses are valid and unexpired.
4. The system validates that the auction window for the load is still open.
5. The system records the bid against the load and timestamps it.
6. The system notifies the Shipper that a new bid has been submitted.
7. The system updates the load listing to reflect the new bid count and current best offer.
8. The Carrier receives confirmation that their bid was successfully submitted.

---

### Alternate Flow: Bid Submitted After Auction Deadline
**Trigger:** At step 4, the system detects that the auction window for the load has already closed.

1. The system rejects the bid submission.
2. The system displays an error message to the Carrier: "Bidding for this load has closed."
3. The system does not record the bid or notify the Shipper.
4. The Carrier is redirected to browse other currently open load listings.
5. Use case ends without completion.

---

### Alternate Flow: Unverified Carrier Permits (optional second alternate flow)
**Trigger:** At step 3, the included Verify Carrier Permits check fails (expired or missing permits).

1. The system blocks the bid submission.
2. The system displays an error message: "Your carrier permits are expired or unverified. Please update your documents before bidding."
3. The Carrier is redirected to their account/document upload page.
4. Use case ends without completion.