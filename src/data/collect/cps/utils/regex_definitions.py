
class RegexDefinitions:
    dateRegex = '(?<!0-9)(\d{1,2}.\s*\d{1,2}.\s*\d{4}\.{0,1})'
    daysListRegex = '(?<!0-9)(\d{1,2}\.\s*\,\s*)+' + dateRegex
    daysRangeRegex = '(?<!0-9)\d{1,2}\.\s*(-|do)\s*' + dateRegex
    daysRangeDiffMonthRegex = '(?<!0-9)(\d{1,2}\.\s*){2}(-|do)\s*' + dateRegex