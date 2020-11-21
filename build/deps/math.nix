let
  seconds_in_1_year = 31557600;
  unix_ts = builtins.currentTime;
in
  rec {
    currentYear = 1970 + unix_ts / seconds_in_1_year;
    currentYearStr = builtins.toString currentYear;
  }
