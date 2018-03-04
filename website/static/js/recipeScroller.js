$(function () {

    var switchTime = 3000;
    const recipeLinks = [
        "https://www.foodnetwork.com/recipes/food-network-kitchen/apple-pie-recipe-2011423",
        "https://www.thespruce.com/classic-and-easy-chocolate-cake-recipe-995137",
        "http://www.geniuskitchen.com/recipe/the-best-biryani-177830",
        "https://www.bettycrocker.com/recipes/ultimate-chocolate-chip-cookies/77c14e03-d8b0-4844-846d-f19304f61c57",
        "https://www.foodnetwork.com/recipes/jerk-chicken-recipe0-1908640"
    ];

    var i = 1;
    var input = $('#recipeLinkInput');
    input.attr("placeholder", recipeLinks[0]);
    window.setInterval(function() {
        input.attr("placeholder", recipeLinks[i]);
        i = (i + 1) % recipeLinks.length;
    }, switchTime);
});

