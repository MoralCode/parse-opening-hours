This parser works using defined patterns to recognize as many of the most common formats for opening hours as possible. These paterns begin with small, fairly trivial patterns and begin combining them into larger and more complex patterns.

Some of these trivial patterns include things like:
- numbers (used for hours and minutes)
- separating characters of various types (like `:` for time)
- plurals (Mondays, Monday, Monday's, Mondays')
- dots (A.M. vs AM)

These are used to build patterns for increasingly complex things like:
- Times
- Days of the week
- common shortcuts (24/7, weekdays)
- common word-based separators (to, through, thru, and)

As things continue getting combined, three primary patterns start emerging. These are known throughout this project as the "range", "list", and "shortcut"

![A diagram showing the basics of range list and shortcut types](Opening%20Hours%20Anatomy-Types.png)

**Range** patterns are used for strings similar to "9am to 5pm" where you generally have two times or days separated by a symbol (i.e. `-`) or word (i.e. `through`) indicating that any time or day between the two specified is valid. 

**List** patterns are used for strings similar to "Monday, Wednesday" where a defined set of days or time ranges are being listed. Single values, like "Monday" can also be seen as a list of one item.

**Shortcut** patterns are used for strings that represent common shortcuts, such as "every day". In this instance "every day" is a shortcut which means the same as listing all 7 days of the week.


Ultimately, the goal of all of these pieces is to assist with breaking down a string containing business opening hours into something that is more easily able to be parsed by a computer. At a high level it looks something like this:

![A high-level breakdown of how some opening hours strings are structured](Opening%20Hours%20Anatomy-General%20Anatomy-v2.png)


Once these patterns are identified using `pyparsing`, they are then parsed out using the `from_parse_results` methods on the respective model classes for that specific type. These classes provide functionality that makes manipulating those types easier, such as converting times from 12 to 24-hour format.
