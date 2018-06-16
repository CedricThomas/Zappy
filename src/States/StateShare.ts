interface Value {
    [name: string]: any
}

export default class StateShare {
    private values: Value;

    constructor() {
        this.values = {};
    }

    addKey(name: string, val: any) {
        this.values[name] = val;
    }

    delKey(name: string) {
        this.values[name] = undefined;
    }

    getKey(name: string): any {
        return this.values[name];
    }

    getSocket() : SocketIOClient.Socket {
        return this.values["socket"];
    }
}