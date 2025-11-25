# Example Test Suite - ReAct Agent Based

## Step 1: Navigate to homepage
- Action: navigate to https://example.com
- Verify: title contains "Example Domain"
- Verify: url contains "example.com"

## Step 2: Check page heading and content
- Action: get the text of the h1 element
- Verify: "h1" visible
- Verify: "h1" text contains "Example Domain"

## Step 3: Verify paragraph and links
- Action: scroll to the first paragraph element
- Verify: "p" visible
- Verify: "a" visible
- Action: get the href attribute of the first link

## Step 4: Complex interaction test
- Action: hover over the first link on the page
- Action: wait for 1000 milliseconds
- Verify: "a[href]" visible
