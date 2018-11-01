app
/**
 * Controller per la gestione dei link e la visualizzazione delle loro informazioni
 * @module typeController
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 * @param {Object} $mdSidenav Il servizio {@link https://material.angularjs.org/latest/api/service/$mdSidenav|$mdSidenav}
 * permette linterazione con le Sidenavs
 */
.controller("typeController", function($scope, $mdDialog, Labels, $mdSidenav) {

    $scope.domini = Labels.domini;
    $scope.nomeProgetto = Labels.nomeProgetto;
    $scope.a = "ddddddddddddddddddddddddddd";
    console.log($scope.domini);
    console.log($scope.nomeProgetto);

    /**
     * Mostra la Sidenav sinistra con i domini
     * @function openLeftMenu
     */
    $scope.openLeftMenu = function() {
        $mdSidenav('left').toggle();
    };

    /**
     * Rimuove il domini con indice ind
     * @function removeDom
     * @param {Number} ind indice del dominio da rimuovere
     */
    $scope.removeDom = function (ind) {
        Labels.domini.splice(ind, 1);
    };

    /**
     * Mostra la finestra modale per la visualizzione delle informazioni del dominio cliccato dall'utente
     * @function showInfo
     * @param {event} $event Click dell'utente sul dominio
     * @param {Object} dom Domini di cui mostrare le informazioni
     */
    $scope.showInfo = function ($event, dom) {
        $mdDialog.show({
            locals:{dom: dom},
            targetEvent: $event,
            templateUrl: 'static/source/templates/infoTypeModal.html',
            windowClass: 'modal-content',
            controller: infoTypeCtrl,
            clickOutsideToClose: true
            }
        )
    };

    function infoTypeCtrl($scope, dom) {

        $scope.dom = dom;
        $scope.domini = Labels.domini;

        /**
         * Rimuove l'intervallo di validita del dominio con indice ind
         * @function removeIntervallo
         * @param {Number} ind Indice del dominio da eliminare
         */
        $scope.removeIntervallo = function (ind) {
            $scope.dom.valori.splice(ind, 1);
        };

        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        }
    }

    /**
     * Inserisce un nuovo dominio
     * @function addNewType
     * @param {event} $event Click dell'utente sul dominio
     */
    $scope.addNewType = function($event) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/typeDefinitionModal.html',
            windowClass: 'modal-content',
            controller: typeCtrl,
            clickOutsideToClose: true
        });
    };

    function typeCtrl($scope, $mdDialog, Labels) {
        $scope.tipiBase = Labels.tipiBase;
        $scope.domini = Labels.domini;
        $scope.intervalli=[];
        $scope.enum = [];
        var inserisci = true;

        /**
         * Resetta i campi del dominio
         * @function reset
         */
        $scope.reset = function () {
            $scope.newTypeName = null;
            $scope.newTypeDefault = null;
            $scope.interDa = null;
            $scope.interA = null;
            $scope.magDi = null;
            $scope.minDi = null;
            $scope.intervalli = [];
            $scope.enum = [];
        };

        /**
         * aggiunge un nuovo tipo
         * @function nuovoTipo
         */
        $scope.nuovoTipo= function () {

            // controllo se il nome è di un tipo già definito
            Labels.domini.forEach(function (t) {
                if (t.nome === $scope.domini) {
                    alert("il tipo con nome " + t.nome + " esiste già");
                    inserisci = false;
                }
            });

            if ($scope.newTypeGen === "enum" && $scope.enum.length === 0) {
                inserisci = false;
                alert("Inserire almeno un elemento nella lista");
            }

            // se ok --> inserimento
            if (inserisci){
                if ($scope.newTypeGen === "enum"){
                    if ($scope.sel === undefined)
                        var newType = {nome: $scope.newTypeName, generico: $scope.newTypeGen, default: null, valori: $scope.enum};
                    else
                        var newType = {nome: $scope.newTypeName, generico: $scope.newTypeGen, default: $scope.enum[$scope.sel], valori: $scope.enum};
                }
                else{
                    if ($scope.newTypeDefault === undefined || $scope.newTypeDefault === "" || $scope.newTypeDefault === null)
                        var newType = {nome: $scope.newTypeName, generico: $scope.newTypeGen,
                            default: null, valori: $scope.intervalli};
                    else
                        var newType = {nome: $scope.newTypeName, generico: $scope.newTypeGen,
                            default: $scope.newTypeDefault, valori: $scope.intervalli};
                }
                Labels.domini.push(newType);
                $scope.reset();
            }
        };

        /**
         * Inserisce un intervallo di validità del tipo
         * @function insIntervalli
         */
        $scope.insIntervalli = function () {
            //controllo estremi e definizione dell'intervallo
            if ($scope.sceltaVinc === "intervallo"){
                if ($scope.interDa <= $scope.interA) {
                    if ($scope.estremoDaIncl && $scope.estremoAIncl) var intervallo = "value >= " + $scope.interDa + " and value <= " + $scope.interA;

                    else if ($scope.estremoDaIncl && !$scope.estremoAIncl) var intervallo = "value >= " + $scope.interDa + " and value < " + $scope.interA;

                    else if (!$scope.estremoDaIncl && $scope.estremoAIncl) var intervallo = "value > " + $scope.interDa + " and value <= " + $scope.interA;

                    else var intervallo = "value > " + $scope.interDa + " and value < " + $scope.interA;
                }else{
                    alert("L'estremo inferiore deve essere minore o uguale di quello superiore");
                    return
                }
            }
            else if ($scope.sceltaVinc === "maggiore"){
                if ($scope.estremoMag) var intervallo = "value >= " + $scope.magDi;
                else var intervallo = "value > " + $scope.magDi;
            }
            else if ($scope.sceltaVinc === "minore"){
                if ($scope.estremoMin) var intervallo = "value <= " + $scope.minDi;
                else var intervallo = "value < " + $scope.minDi;
            }

            // se il nuovo intervallo è gia presente non si inserisce
            if (($scope.intervalli.length === 0 || !$scope.intervalli.includes(intervallo)) &&
                ($scope.interDa !== null || $scope.interA !== null || $scope.magDi !== null || $scope.minDi !== null))
                $scope.intervalli.push(intervallo);

            //reset campi degli intervalli
            $scope.interDa = null;
            $scope.estremoDaIncl = false;
            $scope.interA = null;
            $scope.estremoAIncl = false;
            $scope.magDi = null;
            $scope.estremoMag = false;
            $scope.minDi = null;
            $scope.estremoMin = false;
        };

        /**
         * Rimuove intervallo per i tipi con indice ind
         * @function removeIntervallo
         * @param {Number} ind Indice dell'intervallo da eliminare
         */
        $scope.removeIntervallo = function (ind) {
            $scope.intervalli.splice(ind, 1);
        };

        // GESTIONE DELLE ENUMERAZIONI

        // aggiunge l'elemento alla lista
        /**
         * Aggiunge un elemento ad una enumerazione creata dall'utente
         * @function addElem
         */
        $scope.addElem = function() {
            if ($scope.nomeApp === undefined || $scope.nomeApp === null || $scope.nomeApp === ""){
                return;
            }
            else if (!$scope.enum.includes($scope.nomeApp)){
                $scope.enum.push($scope.nomeApp);
            }
            else {
                alert("Elemento giè esistente");
                return
            }
            $scope.nomeApp = undefined;
        };

        /**
         * Rimuove l'elemento dell'enumerazione con indice ind
         * @param {Number} ind indice dell'elemento da eliminare
         */
        $scope.removeElem = function (ind) {
            $scope.enum.splice(ind, 1);
        };

        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        }
    }
    });