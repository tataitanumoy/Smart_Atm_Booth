$(document).ready(function () {
   // GetTotalUsageGraph("");
    GetWeather("Kolkata");
    GetTotalUsageGraph("monthly");
    // $("#ddGraphType").on("change",function(e){
    //    var a= $("#ddGraphType").val();
    //    var b= $(this).val();
    //     debugger;
    //     GetTotalUsageGraph($(this).val());
    
    // })
})

function GetTotalUsageGraph(type){
    debugger;
    $.ajax({
        method: "POST",
        url: "./api/gettotalusage",
        contentType: "application/json",
      })
      .done(function(dataset) {
        CreateUltrasonicVsTimeLineGraph(dataset);
        
        CreateTempVsTimeGraph(dataset,type);
      });
}
function MonthlyGraph(dataset)
{
    var LineChartData= [];
    dataset.forEach(function(element){
        element.monthyear= element.time.substring(0,7);
    });
    var months = [];
    var groupbyMonth = _.groupBy(dataset, function(a){
        if(months.indexOf(a.monthyear)== -1)
        {
            months.push(a.monthyear)
        }
        return a.monthyear
    });
    debugger;
  
        for (var i=0;i<months.length;i++)
            {
                var sumOfTemp=0;
                for(var j=0;j<groupbyMonth[months[i]].length;j++)
                {
                    sumOfTemp += Number(groupbyMonth[months[i]][j].temp);
                }
                var tempAvg = sumOfTemp/groupbyMonth[months[i]].length;
                var obj = {Temperaturevalue:tempAvg, Time:months[i]};
                LineChartData.push(obj);
            }
 return LineChartData;   
    
}
function YearlyGraph(dataset)
{
    var LineChartData= [];
    dataset.forEach(function(element){
        element.monthyear= element.time.substring(0,4);
    });
    var years = [];
    var groupbyYear = _.groupBy(dataset, function(a){
        if(years.indexOf(a.monthyear)== -1)
        {
            years.push(a.monthyear)
        }
        return a.monthyear
    });
    debugger;
  
        for (var i=0;i<years.length;i++)
            {
                var sumOfTemp=0;
                for(var j=0;j<groupbyYear[years[i]].length;j++)
                {
                    sumOfTemp += Number(groupbyYear[years[i]][j].temp);
                }
                var tempAvg = sumOfTemp/groupbyYear[years[i]].length;
                var obj = {Temperaturevalue:tempAvg, Time:years[i]};
                LineChartData.push(obj);
            }
 return LineChartData;   
    
}
// Craete line graph
function CreateTempVsTimeGraph(dataset,type){
    
    var  LineChartData= [];
    if(type == "month")
    {
         LineChartData = MonthlyGraph(dataset); 
    }
    else if(type == "year")
    {
         LineChartData = YearlyGraph(dataset); 
    }
   else
   {
    for (var i=0;i<dataset.length;i++)
           {
                
                var obj = {Temperaturevalue:dataset[i].temp, Time:dataset[i].time};
                LineChartData.push(obj);
           }
   }
    
    if(LineChartData!=null){
            debugger;       
    Morris.Line({
        element: 'graph-area',
        data:LineChartData,
        xkey: 'Time',
        ykeys: ['Temperaturevalue'],
        labels: ['Temperature data']
      });
   }
  
}
// Craete line graph
function CreateUltrasonicVsTimeLineGraph(dataset){
    var LineChartData=[];
    if(dataset!=null){
        for (var i=0;i<dataset.length;i++)
            {
                var obj = {Ultrasonicvalue:dataset[i].ultrasonic,time:dataset[i].time};
                LineChartData.push(obj);
            }
    //     dataset.reduce(function(res, value) {
    //     if (!res[value.PostalCode]) {
    //     res[value.PostalCode] = { PostalCode: value.PostalCode, TotalGallons: 0 };
    //     barChartData.push(res[value.PostalCode])
    //     }
    //     res[value.PostalCode].TotalGallons = Number(res[value.PostalCode].TotalGallons) + Number(value.TotalGallons.replace(/,/g, ''));
    //     return res;
    // }, {});
    Morris.Line({
        element: 'graph-tu_vs_pc',
        data:LineChartData,
        xkey: 'time',
        ykeys: ['Ultrasonicvalue'],
        labels: ['Ultrasonic Data']
      });
   }
  
}

function GetWeather(location){
   var weatherAPI="http://api.openweathermap.org/data/2.5/weather?q=";
   var appId="&appid=ecb1f756686518281c429bf5b7498d70";
   $.get(weatherAPI+location+appId,function(response){
        $("#location").html(response.name);
        $("#weatherTemp").html(GetCelsius(response.main.temp).toString().split('.')[0]);
        $("#weatherStatus").html(response.weather[0].main);
        // var Icon="https://openweathermap.org/img/w/"+ response.weather[0].icon +".png";
        // var Humidity=response.main.humidity
    })
 }
function GetCelsius(temp) {
    return  temp - 273;
  };