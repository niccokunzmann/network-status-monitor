
/*
devices:
1x router
2x av600
1x netgear

*/
var NO_DEVICES_DEFAULT = 0;


var names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
var weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];


var colors = {
  "Mon" : "red",
  "Tue" : "green",
  "Wed" : "blue",
  "Thu" : "orange",
  "Fri" : "brown",
  "Sat" : "purple",
  "Sun" : "yellow",
};

var charts = [];

function toggleWeekday(day) {
  var index = names.indexOf(day);
  if (index < 0) {
    console.log("Cannot toggle " + day);
    return;
  }
  document.body.classList.toggle("inactive" + day);
  var active = !document.body.classList.contains("inactive" + day);
//  console.log("toggle " + day + " at index " + index + ": " + (active ? "active" : "inactive"));
  for (var i = 0; i < charts.length; i++) {
    // toggle the visibility
    // see https://stackoverflow.com/a/49252102
    var chart = charts[i];
    // see https://www.chartjs.org/docs/2.7.3/configuration/legend.html
    var meta = chart.getDatasetMeta(index);
//    console.log(meta);
    meta.hidden = !active;
    chart.update();
  }
}

function showDays(xValues, values) {
  var datasets = [];
  for (var i = 0; i < values.length; i++) {
        datasets.push({
        data: values[i],
        borderColor: colors[names[i]],
        fill: false
      });
  }
  charts.push(new Chart("wholeDay", {
    type: "line",
    data: {
      labels: xValues,
      datasets: datasets,
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Internet Availability by Time in %"
      }
    }
  }));
}



function setDownloadSpeed(xValues, values) {
  var datasets = [];
  for (var i = 0; i < values.length; i++) {
        datasets.push({
        data: values[i].map(function(v){return v / 1000;}),
        borderColor: colors[names[i]],
        fill: false
      });
  }
  charts.push(new Chart("downloadSpeed", {
    type: "line",
    data: {
      labels: xValues,
      datasets: datasets,
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Download Speed in kb/s"
      }
    }
  }));
}



function setDevices(xValues, values) {
  var datasets = [];
  for (var i = 0; i < values.length; i++) {
        datasets.push({
        data: values[i].map(function(v){return Math.max(0, v - NO_DEVICES_DEFAULT);}),
        borderColor: colors[names[i]],
        fill: false
      });
  }
  charts.push(new Chart("devices", {
    type: "line",
    data: {
      labels: xValues,
      datasets: datasets,
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Devices in the Network"
      }
    }
  }));
}






function showWeekOverview(yValues) {
//  console.log("weekly" + JSON.stringify(yValues));
  var barColors = [colors.Mon, colors.Tue, colors.Wed, colors.Thu, colors.Fri, colors.Sat, colors.Sun];
  for (var i = 0; i < weekdays.length; i++) {
    var element = document.getElementById("percent" + names[i]);
    element.innerHTML = "<br/>" + yValues[i] + "%";
  }

/*  charts.push(new Chart("weekOverview", {
    type: "doughnut",
    data: {
      labels: weekdays,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Weekly Overview of Internet Availability in %"
      }
    }
  })); */
}

var STATUS = [
  {
    message: "No Internet in the barn since ",
    cls: "noInternet"
  },
  {
    message: "Internet worked in the barn",
    cls: "okInternet"
  },
  {
    message: "No Data",
    cls: "noData"
  }
]

function secondsToString(seconds) {
  var result = seconds % 60 + "sec";

  var minutes = Math.floor(seconds / 60);
  if (minutes >= 1) {
    result = minutes % 60 + "min " + result;
  }

  var hours = Math.floor(minutes / 60);
  if (hours >= 1) {
    result = hours % 24 + "h " + result;
  }

  var days = Math.floor(hours / 24);
  if (days >= 1) {
    result = days + "d " + result;
  }
  return result;
}

function setCurrentStatus(lastSuccess, statusId, lastUpdate) {
  var element = document.getElementById("currentStatus");
  var status = STATUS[statusId];
  element.classList.add(status.cls);
  element.innerText = status.message + " " + secondsToString(lastSuccess) + " ago." + (statusId == 0 ? " Last updated " + secondsToString(lastUpdate) + " ago." : "");
//  console.log(element.classList);
}
