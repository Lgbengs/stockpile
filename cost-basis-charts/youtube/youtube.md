# YouTube Script: "Visualize Your Position's Cost Basis with Claude Code"

## Title
Charts Your Broker Doesn't Show You (Using Claude Code)

## Thumbnail Ideas

Done - Choosing #1

**Concept 1 — The Chart IS the Thumbnail** *(recommended)*
Background: screenshot of the Midnight-scheme chart (dark navy,
blue/orange lines). Bold white text overlaid:
- Large: Chart YOUR REAL COST BASIS
- Small (bottom): Build it with Claude Code

Give Gemini: the chart screenshot + "make a YouTube thumbnail with
bold white text 'YOUR REAL COST BASIS' in the upper third and small
text 'Built with Claude Code' at the bottom, keep the chart visible"

**Concept 2 — Split / Contrast**
Left half: greyed-out brokerage account view. Right half: colorful
chart. Bold text across the center:
- vs. THIS

Give Gemini: both images side by side + "YouTube thumbnail split
screen, left side desaturated/grey, right side vibrant, bold text
'vs. THIS' across the middle"

**Concept 3 — The Hook**
Dark background, your face (surprised/impressed) on one side, chart
on the other. Text:
- YOUR BROKER HIDES THIS

Give Gemini: your photo + chart screenshot + "YouTube thumbnail, face
on left looking surprised, chart on right, bold red/white text 'YOUR
BROKER HIDES THIS' at the top"

---

## HOOK (0:00–1:30)

*[10 Animation: chart fly-in — close price line draws left to right,
then adjusted cost basis line draws underneath it, transaction
markers pop in, right-edge labels appear showing P&L]*

DONE -----

This episode is all about charting your positions with Claude Code.
It's related to my last episode about making Google Sheets for your
positions with Claude Code, linked in the description.

We're gonna once again use transaction logs from your brokerage,
but this time we'll visualize your position performance with charts.

Borrowing the theme from last episode, the charts in this episode
will show you something your brokerage account doesn't — your positions
*real* performance.

[11 Switch to a real chart]

DONE -----

Here's the more complex underlying chart to the animation we just watched.
We'll dive deeper into this chart later in the episode.

It visualizes every call and put you've ever bought or sold,
every dividend you've collected, and every time you've bought and
sold shares.  This information will be in the transaction logs
you'll download from your brokerage.

I built this entire thing without writing a single line of code,
I just described what I wanted, and Claude wrote all the
code to
 - produce these charts
 - document them.
 - it even suggested the free charting tool to use.

[12 Back to Animation]

DONE -----

Back to the animation...

This is Claude Design, a new product that comes with Claude Code.
I simply asked it to animate one of the static charts I generated.

And you're seeing the results. This was my first
experiment with Claude Design, and I'm looking forward to using it more
in the future.

---

## SETUP THE PROBLEM (1:30–2:10)

[13 Show actual chart]

DONE -----

Now back to the detailed Cost Basis Chart

Most people look at their brokerage account and see a table or chart
showing a simple average cost per share. We'll do better.
These charts will enhance your typical broker's position view with every
transaction related to each of your positions. The Python script
parses your transaction history, runs First In, First Out accounting
on every trade, and subtracts all the income you've collected. Each
of the lines you see here is a view of a different metric measuring how
profitable your position is.

It also includes the real historical price from Yahoo
Finance, this top blue line.  So you can see the full picture at a glance.

[20 dividends on chart]

Before we really dig in to the features of the chart,
let's see how to add a feature to the chart with Claude.

The orange and green lines here and here,
have dots that represent events.
Some of these events are dividends. Lets see if we can mark the dividends
on the chart with a D, to distinguish them from other kinds of events.


---

## LIVE DEMO — ADDING PNG EXPORT (2:10–4:10)
*[Screen: terminal with Claude Code open, chart HTML visible]*

[21 Claude term]

If you look close, you can see I've asked Claude to do that here...
Can you make the Dot a D...

Once I hit enter, Claude goes to work, thinking and changing code....

Claude has completed his first attempt at this, lets see how it looks
by regenerating the charts and viewing...

DONE -----

[22 run]

Here's the command to regenearte the charts...


[23 view chart]

----- DONE

Here's the chart after reloading it.
Look close and you can see all dividend transactions are marked with a D now
and every other kind of transaction is not.

"That's my workflow. 
 - Describe what I want
 - Claude writes it,
 - I confirm and test it.
 - I iterate until I get just what I want
 - No docs, no Stack Overflow, no writing code
 - Easy mode and time savings
 - and I can try out whatever I think of with minimal effort

---

## THE CHART IN DETAIL (4:10–7:40)
*[30 stock price]*

----- Done

Now lets take a closer look at everything on the chart.
Here's the legend so you know what each line is.
They Y axis is price per share
The X axis is date

The blue line here is from Yahoo Finance — that's what
the stock actually traded at each day.  It's final right annotation here,
shows your P/L per share by subtracting the adjusted cost per share
from the current stock price.


*[31 FIFO]*
 
----- Done

The purple line is your stock FIFO cost basis. That's the raw
average cost of your shares based on the order you bought them.
Every time you buy shares, it includes them in
the average. Every time you sell, the oldest lots come off first
and it adjusts.

You can see here, I bought 200 shares of SCHW at 69.90, then
bought another 100 @ 65.  So over on the right you see I have
300 shares with an average price of 68.27

 
---- ^^ Done

[32 Adjusted]

-----Done

the FIFO line only considers stock buys and sells.
It won't adjust for other kinds of transactions.

The orange line, in contrast, is your adjusted cost basis. Every time you 
collect a premium on a covered call or put, or receive a dividend, that income
gets subtracted from your cost. Over time, if you're actively selling
options and/or collecting dividends, you'll see this
line drift lower — meaning your cost basis is less and less, and
it's easier for the position to be profitable. The one exception is
if you sell a debit roll, not a credit, then the line will drift
higher.  For selling options, that means you paid more premium to close out
your old position than you collected to open your new position.

Hover over any dot to see exactly what the transaction was.
And the final right annotation give you your final
adjusted cost per share

[33 income]

This green line and area down at the bottom of the chart is the income
you've received over time per share.  It's almost the exact inverse of 
the orange line, as your income per share normally increases over time.

It's right annotation gives you the final per share and total income
this position has collected.





[34 options]


If you have open covered calls or puts on a position, the chart gets
a few more lines. This green dashed line is the estimate of the 
market value of the open options over time using Black-Scholes 
(linked in the description).
It's added to your adjusted cost basis and plotted here.

So you can see your *true* P/L today. This accounts for what it
would cost to close your open options. 

The dashed horizontal line  here shows your strike price over the lifetime
of your open option — from when you opened it to the current date.
You can see at a glance whether the stock is above or below your strike,
and it's right annotation shows you how many options are open
and its expiration.

[35 intrinsic time value]

Down toward the bottom of the chart alongside the income
you'll also see Intrinsic Value and Time Value lines
for of the open options.

Intrinsic value is how far in the money the option is —
the portion that has real dollar value right now.

Time value is the rest of the options current market value —
it decays to zero as you approach expiration.

Depending on circumstances, Time value can be a great indicator of whether
to close your position. For example, if a covered call is deep ITM and will
likely get called away, then its remaining Time Value will be very small
compared to the position's close out value.  You'd probably be better off
closing the position and using the funds to invest in better yielding cash
or finding another investment opportunity.

This Time Value Yield computed against closeout value is shown
in the far right annotation.

[36 summary]

And that's about all I want say about the chart.
There's a lot of info here, more than you may want or need.
But it's great if you want a better understanding of the performance
of your positions over time.

---

## HOW I BUILT THIS WITH CLAUDE CODE (7:40–8:20)

[40 how]

Now I'm going to say a little more about how I made this,
and then if you're still around,
Please consider liking and subscribing, and then
I'll talk about how you can install and use this for your positions.

for each feature I described what I wanted to Claude, for example: 
 — parse the broker CSVs
 - compute the cost basis,
 - make a line showing this, make another line showing that
 - Annotate this line like this
 - add the historical Yahoo Finance prices,

And on and on, and Claude wrote it. Then I iterated to get just like I wanted.
I tweaked the chart layout, I added things like a dashed line for the
Black-Scholes estimate of the open option, I asked Claude to make it so
so labels don't overlap.  I asked Claude to move the legend to the least used
area of the chart.  And I kept iterating.

[41 code]

---- DONE

It's so much easier than the olden days when I actually had to write this stuff
from scratch.  And Claude is a better coder, documenter, and refactorer
than I ever was.

Speaking of refactor, I also asked Claude to follow some best practice
guidelines for the structure of the project and configuration,
and to refactor the CSV parsing code so it could be shared accross tools.

Claude did an amazing, several nice suggestions, like also refactoring the 
Yahoo Finance calls into a shared space.

---

## WHAT YOU'LL NEED (8:20–8:45)

[50 subscribe]

---- DONE

If you'd like to generate your position charts with your transaction logs,
You'll need to do some setup.  The easy-mode way to do this is to get
a subscription to Claude Code (linked in the description and project README),
and start Claude Code in the stockpile directory after cloning
or downloading the repository.  Then ask it to help you get it running with
your transactions file.

Sadly I am not being sponsored and have no connection to Anthropic other than
loving its tools.

[51 Go to repo]

---- DONE

You'll need:

1. A transaction history export from your brokerage. My repo
   currently supports Schwab and Robinhood, more brokerages soon.
2. you'll need Python and some dependencies installed on your machine,
   see the README for details
   and let Claude help if you have a Claude subscription.
3. And This repo — link in the description, it's free on GitHub.

---

## EXPORTING YOUR TRANSACTIONS (8:45–9:15)
*[52 show input folder]*

=----- Done

Once you've downloaded the full transaction log of an account from your
broker, put it somewhere — the /input sub folder in the stockpile directory works.
As you can see, i have some transaction logs here, several from
Schwab and one from Robinhood.

Make sure you download as many transactions as possible from your broker,
to increase the chances of getting all your position history.  If you don't
have the complete history of a position, it won't know enough to make
an accurate chart.

[53 show creating a copy and editing config]

=----- Done

Then setup your configuration by creating a copy of config.toml.example
and name it config.toml in the cost-basis-charts folder.
Then point that configuration to where ever you put your transactions file
from your brokerage.

---

## RUNNING IT (9:15–10:15)
*[60 Run: Terminal: `uv run cost-basis-charts/run_charts.py`]*

=----- Done

Once you've done all the setup, you'll run it with one command from
the repo root.  It will read the config you just set up, parse your
transactions, pull historical prices from Yahoo Finance, and write an HTML
file for each ticker into the `cost-basis-charts/charts` folder.

*[61 Go to charts folder and open one with Chrome]*

=----- Done

Open one of the charts you just made, and have a look — be sure to
hover the mouse over the lines.

If you want to tweak it, improve or add new features, feel
free! Subscribe to Claude Code, fork my repo, and let us know what
you did.

---

## OUTRO (10:15–10:35)

[70 conclusion]

Link to the repo is in the description — it's all open source. If
you're running covered calls, wheeling, or just want a more complete
picture of your positions' performance, this will help.

Let me know in the comments what other views or features would
be useful, I'd love to hear your ideas about other interesting things
we could do with our transaction logs.  Maybe I'll add toggle for each
line to show or not show.

Please consider liking and subscribing, and have a look at my last
episode which should be showing here soon,
It was about computing position metrics in Google Sheets
from your transaction logs.

---

## RESOURCES (description links)

- Repo: https://github.com/medloh/stockpile
- Black-Scholes explained:
  https://www.investopedia.com/terms/b/blackscholes.asp
- Previous episode (Google Sheets positions tracker):
  https://youtu.be/9uf3cyOWPBQ?si=kRyNK88tkc9qD5o0

Support the work:
- GitHub Sponsors: https://github.com/sponsors/medloh
- Patreon: https://www.patreon.com/OptionsforLongTermInvestors

---

## PRODUCTION NOTES

### Before Recording
- Write the description first — YouTube indexes it for search
- Pick a target keyword phrase ("cost basis covered calls", "Claude
  Code python stock charts") and say it naturally in the first 30s
- Record a strong first 30 seconds — audience retention at 30s is a
  key ranking signal

### Before Publishing
- Add chapters (timestamps in description) — viewers scrub instead
  of leaving, which increases watch time
- Add 3–5 tags matching your target keywords
- Write strong first 2 lines of description — that's what shows
  before "show more" in search results
- Set custom thumbnail BEFORE publishing, not after
- Add cards at ~20%, 40%, 60% of runtime pointing to the Google
  Sheets episode

### Immediately After Publishing (first 48 hours matter most)
- Share to relevant communities:
  - r/options, r/thetagang, r/learnprogramming
  - Claude/AI Discord servers
  Early velocity signals quality to the algorithm
- Pin a comment with the repo link and a seed question:
  "What other charts would be useful?"
- Reply to every early comment — engagement in the first 48 hours
  boosts distribution

### Exit Screens
Go back and add this video to the exit screen of:
- The Google Sheets episode https://youtu.be/9uf3cyOWPBQ?si=3MoC5Mfjvf39ujn0
- Any other popular episodes on your channel
Viewers already interested in your tools are most likely to watch
both.

### Ongoing (2 weeks after)
- Check YouTube Studio analytics
  - If click-through rate is under ~4%, test a new thumbnail
  - If one chapter gets most views, consider a standalone short on
    just that topic
