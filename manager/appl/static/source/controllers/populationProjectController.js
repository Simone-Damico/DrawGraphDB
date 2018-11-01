app

.controller("populationProject", function($scope, $http, $mdDialog, Labels){

    $scope.labels = Labels;

    $scope.choiceFile = function (event) {
        FileList = event.target.files;
        if(FileList.length > 0) {
            File = FileList[0];
            aa = {file: File, nome:File.name};
            FormData = new FormData();
            FormData.append('uploadFile', File);
            console.log("form", FormData);
        }
        $http.post("http://localhost:"+ Labels.porta.toString() + "/popola/", FormData)
            .then(function successCallback(response){
                console.log("Successfully POST-ed data to popolation function");
            }, function errorCallback(response){
                console.log("POST-ing of data failed to population function");
            });
    };

    $scope.popola = function() {
        ss = document.getElementById("file");
        console.log($scope.file);
        $http.post("http://localhost:"+ Labels.porta.toString() + "/popola/", ss)
            .then(function successCallback(response){
                console.log("Successfully POST-ed data to popolation function");
            }, function errorCallback(response){
                console.log("POST-ing of data failed to population function");
            });
    };
});