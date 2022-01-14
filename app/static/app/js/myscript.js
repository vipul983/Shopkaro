$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    // console.log(id);
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            // console.log(data)
            elm.innerText=data.quantity
            document.getElementById('totalamount').innerText= data.totalamount
            document.getElementById('amount').innerText=data.amount
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var elm=this.parentNode.children[2]
    // console.log(id);
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            // console.log(data)
            elm.innerText=data.quantity
            document.getElementById('totalamount').innerText= data.totalamount
            document.getElementById('amount').innerText=data.amount
        }
    })
})

$('.delete-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var elm=this
    // console.log(id);
    $.ajax({
        type:"GET",
        url:"/deletecart",
        data:{
            prod_id:id
        },
        success:function(data){
            // console.log(data)
            elm.parentNode.parentNode.parentNode.parentNode.remove()
            document.getElementById('totalamount').innerText= data.totalamount
            document.getElementById('amount').innerText=data.amount
        }
    })
})