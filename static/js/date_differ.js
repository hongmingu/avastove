
    var date_differ = function date_differ(datetime){
        var minute_unit = 1000 * 60; // hour
        var hour_unit = 1000 * 60 * 60; // hour
        var day_unit = 1000 * 60 * 60 * 24;// day
        var month_unit = 1000 * 60 * 60 * 24 * 30;// month
        var year_unit = 1000 * 60 * 60 * 24 * 30 * 12; // year
        var current_time = new Date();
        var target_time = new Date(datetime);
        var difference = current_time - target_time
        if (difference < minute_unit){
            return 'just now'
        } else if (minute_unit <= difference && difference < 2 * minute_unit){
            return 'a minute ago'
        } else if (2 * minute_unit <= difference && difference < hour_unit) {
            return parseInt(difference/minute_unit) + ' minutes ago'
        } else if (hour_unit <= difference && difference < 2 * hour_unit) {
            return 'a hour ago'
        } else if (2 * hour_unit <= difference && difference < day_unit) {
            return parseInt(difference/hour_unit) + ' hours ago'
        } else if (day_unit <= difference && difference < 2 * day_unit) {
            return 'a day ago'
        } else if (2 * day_unit <= difference && difference < month_unit) {
            return parseInt(difference/day_unit) + ' days ago'
        } else if (month_unit <= difference && difference < 2 * month_unit) {
            return 'a month ago'
        } else if (2 * month_unit <= difference && difference < year_unit) {
            return parseInt(difference/month_unit) + ' months ago'
        } else if (year_unit <= difference && difference < 2 * year_unit) {
            return 'a year ago'
        } else if (2 * year_unit <= difference) {
            return parseInt(difference/year_unit) + ' years ago'
        }
    }