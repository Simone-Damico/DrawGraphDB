app

/**
 * Servizio per la gestione dei dati inseriti dall'utente nel grafo
 * @namespace Labels
 * @property {String} nomeProgetto Il nome del progetto
 * @property {String} nomeDB Il nome del database
 * @property {String} descrizioneProgetto La descrizione del progetto
 * @property {String} dbms Il tipo di DBMS
 * @property {Number} porta Il numero di porta http del progetto
 * @property {Path} projectFolder Il path del progetto
 * @property {Date} createdDate La data di creazione
 * @property {Object[]} nodes I nodi del grafo
 * @property {Object[]} links Gli archi del grafo
 * @property {String[]} tipiBase I tipi base per la definizione dei domini
 * @property {Object[]} domini I domini dei dati
 * @property {String[]} molteplicità Le molteplicità degli archi
 * @property {String[]} supportedDB I DBMS supportati
 */
.service('Labels', function(){

    /**
     * Il nome del progetto
     * @type {string}
     */
    this.nomeProgetto = "nomea";

    /**
     * Il nome del database del progetto
     * @type {string}
     */
    this.nomeDB = "nomeData";

    /**
     * La descrizione del progetto
     * @type {string}
     */
    this.descrizioneProgetto = "questo progetto è una prova";

    /**
     * Il tipo di DBMS del progetto
     * @type {string}
     */
    this.dbms = "SQLite";

    /**
     * Il numero di porta http del progetto
     * @type {Number}
     */
    this.porta = null;

    /**
     * Il path del progetto
     * @type {Path}
     */
    this.projectFolder = null;

    /**
     * La data di creazione del progetto
     * @type {Date}
     */
    this.createdDate = null;

    /**
     * I nodi del grafo
     * @type {Object[]}
     */
    this.nodes = [
        {id: 0, reflexive: false, nome: "nodo 1", proprieta: [{nomeProp: "nomeProp1_1", dominio: "int", notNull: true, default: "1", intervalli:[]},
                                                        {nomeProp: "nomeProp1_2", dominio: "sesso", notNull: false, default: "Maschio", intervalli:[]},
                                                        {nomeProp: "nomeProp1_3", dominio: "int", notNull: false, default: "6", intervalli:[]},
                                                        {nomeProp: "nomeProp1_4", dominio: "int", notNull: true, default: null, intervalli:[]},
                                                        {nomeProp: "nomeProp1_5", dominio: "int", notNull: true, default: null, intervalli:[]}],
                                                primaryKey: null, secondarykey:[]},

        {id: 1, reflexive: false, nome: "nodo 2", proprieta: [{nomeProp: "nomeProp2_1", dominio: "int", notNull: true, default: "12", intervalli:[]},
                                                        {nomeProp: "nomeProp2_2", dominio: "date", notNull: false, default: null, intervalli:[]}],
                                                primaryKey:null, secondarykey:[]},

        {id: 2, reflexive: false, nome: "nodo 3", proprieta: [], primaryKey:[], secondarykey:[]}
        ];

    /**
     * Gli archi del grafo
     * @type {Object[]}
     */
    this.links = [
        {id: 0, source: this.nodes[0], target: this.nodes[1], left: false, right: true, nome:"link_1",
            molteplicita: {source: "0 - N", target: "0 - N"}, primaryKey:[], secondarykey:[],
            proprieta: [{nomeProp: "nomeProplink1_1", dominio: "int", notNull: true, default: "12", intervalli:[]},
                        {nomeProp: "nomeProplink1_2", dominio: "int", notNull: true, default: "1552", intervalli:[]}] },

        {id: 1, source: this.nodes[0], target: this.nodes[2], left: false, right: true, nome:"link_2",
            molteplicita: {source: "0 - 1", target: "0 - 1"}, primaryKey:[], secondarykey:[],
            proprieta: [{nomeProp: "nomeProplink2_1", dominio: "int", notNull: true, default: "5.64", intervalli:[]},
                        {nomeProp: "nomeProplink2_2", dominio: "float", notNull: true, default: "5.88", intervalli:[]}] },

        {id: 2, source: this.nodes[1], target: this.nodes[2], left: false, right: true, nome:"link_3",
            molteplicita: {source: "1 - 1", target: "0 - N"}, primaryKey:[], secondarykey:[],
            proprieta: [{nomeProp: "nomeProplink3_1", dominio: "float", notNull: true, default: "10.10", intervalli:[]}] }
        ];

    this.lastNodeId = this.nodes.length - 1;
    this.lastLinkId = this.links.length - 1;

    /**
     * I tipi base per la definizione dei domini
     * @type {string[]}
     */
    this.tipiBase=["int", "float", "string", "bool", "date", "enum"];

    /**
     * I domini dei dati
     * @type {Object[]}
     */
    this.domini=[
        {nome: "int", generico: "int", default: "0", valori: []},
        {nome: "float", generico: "float", default: "0.0", valori: []},
        {nome: "string", generico: "string", default: null, valori: []},
        {nome: "bool", generico: "bool", default: null, valori: []},
        {nome: "date", generico: "date", default: null, valori: []},
        {nome: "dom1", generico: "int", default: 5, valori: ["value > 2"]},
        {nome: "sesso", generico: "enum", default: "Maschio", valori: ["Maschio", "Femmina"]}];

    this.operatoriConfronto = ["uguale","diverso","minore","maggiore","minore-uguale","maggiore-uguale"];

    /**
     * Le molteplicità degli archi
     * @type {string[]}
     */
    this.molteplicita=["0 - 1", "0 - N", "1 - 1", "1 - N"];

    /**
     * I DBMS supportati
     * @type {string[]}
     */
    this.supportedDB = ["MySQL", "Neo4j", "SQLite"];

});