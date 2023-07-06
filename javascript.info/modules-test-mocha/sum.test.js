import {sum} from './sum.js';


describe('sum', function () {
    it('should return sum of arguments', function () {
        assert(sum(1, 2), 3);
    });
});
