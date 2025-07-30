class Calculator {
    constructor() {
        this.value = 0;
    }
    
    add(x) {
        this.value += x;
        return this.value;
    }
}