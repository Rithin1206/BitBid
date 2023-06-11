function round(number) {
    return number.toFixed(2);
}

$(document).ready(function() {
    // for some reason jquery isn't working well in finding elems
    // let's stick to plain JS for now.
    // TODO: use jquery instead of JS
    var $input = document.getElementsByClassName('input-bid')[0]; 
    minimum_bid = Math.max(highest_bid+increment,base+increment);
    $input.value = round(minimum_bid);

    var minusButton = document.getElementsByClassName('minus')[0];
    var plusButton = document.getElementsByClassName('plus')[0];
    minusButton.addEventListener('click',function(event) {
        event.preventDefault();
        $input.value = round(Math.max(minimum_bid, parseFloat($input.value) - increment));
    },false);
    plusButton.addEventListener('click',function(event) {
        event.preventDefault();
        $input.value = round(parseFloat($input.value) + increment);
    },false);
});