var commissions = {}
var commissions1 = {}

function commissionChange(commissionEl, commissionPercentEl, offerPrice, idx) {
  if(idx === 0) {
      commissionEl.change(function(e){
          if (e.target.value != ""){
            var commissionPercentElVal = (parseInt(e.target.value.replace(',', '')) / parseInt(offerPrice.val().replace(',', ''))) * 100;
            commissionPercentEl.val(commissionPercentElVal.toFixed(2));
        }
      })

  } else if (idx === 1) {
      commissionPercentEl.change(function(e){
        if (e.target.value != ""){
            targetValue = e.target.value
            var commissionElVal =  parseInt(offerPrice.val().replace(',', '')) / 100 * parseFloat(e.target.value);
            commissionEl.val(Math.trunc( commissionElVal ));
        }
      })

  } else if ( idx === 2) {
    targetValue = commissionPercentEl.val()
    if (targetValue != ""){
        var commissionElVal =  parseInt(offerPrice.val().replace(',', '')) / 100 * parseFloat(targetValue);
        commissionEl.val(Math.trunc( commissionElVal ));
    }
  }
};



if($('#offer-cards').attr('data-no-commission-choices') === 'true') {

    $('#btn_0_final_price').click(function(){
        $('#wrap_0_commission_buyer').toggle()
        $('#wrap_0_commission_buyer_percent').toggle()
    if($('#toggle_0_down').hasClass('fa-angle-down')) {
        $('#toggle_0_down').removeClass('fa-angle-down')
        $('#toggle_0_down').addClass('fa-angle-up')
    }else{
        $('#toggle_0_down').removeClass('fa-angle-up')
        $('#toggle_0_down').addClass('fa-angle-down')
    }
    });   
    $('#btn_1_final_price').click(function(){
        $('#wrap_1_commission_buyer').toggle()
        $('#wrap_1_commission_buyer_percent').toggle()
    if($('#toggle_1_down').hasClass('fa-angle-down')) {
        $('#toggle_1_down').removeClass('fa-angle-down')
        $('#toggle_1_down').addClass('fa-angle-up')
    }else{
        $('#toggle_1_down').removeClass('fa-angle-up')
        $('#toggle_1_down').addClass('fa-angle-down')
    }
    });   

        var commissionEl = 'commissionElbuyer0'
        var commissionPercentEl = 'commissionPercentElbuyer0'
        var offerPrice = 'offerPrice0'

        commissions[commissionEl] = $('input[name="form-0-commission_buyer"]')
        commissions[commissionPercentEl] = $('input[name="form-0-commission_buyer_percent"]')

        if($('input[name="form-0-final_price"]').attr('value')) {
        commissions[offerPrice] = $('input[name="form-0-final_price"]')
        } else {
        commissions[offerPrice] = $('input[name="form-0-price"]')
        }

        commissionChange(commissions[commissionEl], commissions[commissionPercentEl], commissions[offerPrice], 0)
        commissionChange(commissions[commissionEl], commissions[commissionPercentEl], commissions[offerPrice], 1)
        commissionChange(commissions[commissionEl], commissions[commissionPercentEl], commissions[offerPrice], 2)

        var commissionEl1 = 'commissionElbuyer1'
        var commissionPercentEl1 = 'commissionPercentElbuyer1'
        var offerPrice1 = 'offerPrice1'

        commissions1[commissionEl1] = $('input[name="form-1-commission_buyer"]')
        commissions1[commissionPercentEl1] = $('input[name="form-1-commission_buyer_percent"]')

        if($('input[name="form-1-final_price"]').attr('value')) {
          commissions1[offerPrice1] = $('input[name="form-1-final_price"]')
        } else {
          commissions1[offerPrice1] = $('input[name="form-1-price"]')
        }

        commissionChange(commissions1[commissionEl1], commissions1[commissionPercentEl1], commissions1[offerPrice1], 0)
        commissionChange(commissions1[commissionEl1], commissions1[commissionPercentEl1], commissions1[offerPrice1], 1)
        commissionChange(commissions1[commissionEl1], commissions1[commissionPercentEl1], commissions1[offerPrice1], 2)
    
        var commissionEl3 = 'commissionElbuyer0'
        var commissionPercentEl3 = 'commissionPercentElbuyer0'
        var offerPrice3 = 'offerPrice0'

        commissions[commissionEl3] = $('input[name="form-0-commission"]')
        commissions[commissionPercentEl3] = $('input[name="form-0-commission_percent"]')

        if($('input[name="form-0-final_price"]').attr('value')) {
        commissions[offerPrice3] = $('input[name="form-0-final_price"]')
        } else {
        commissions[offerPrice3] = $('input[name="form-0-price"]')
        }

        commissionChange(commissions[commissionEl3], commissions[commissionPercentEl3], commissions[offerPrice3], 0)
        commissionChange(commissions[commissionEl3], commissions[commissionPercentEl3], commissions[offerPrice3], 1)
        commissionChange(commissions[commissionEl3], commissions[commissionPercentEl3], commissions[offerPrice3], 2)

        var commissionEl4 = 'commissionElbuyer1'
        var commissionPercentEl4 = 'commissionPercentElbuyer1'
        var offerPrice4 = 'offerPrice1'

        commissions1[commissionEl4] = $('input[name="form-1-commission"]')
        commissions1[commissionPercentEl4] = $('input[name="form-1-commission_percent"]')

        if($('input[name="form-1-final_price"]').attr('value')) {
          commissions1[offerPrice4] = $('input[name="form-1-final_price"]')
        } else {
          commissions1[offerPrice4] = $('input[name="form-1-price"]')
        }

        commissionChange(commissions1[commissionEl4], commissions1[commissionPercentEl4], commissions1[offerPrice4], 0)
        commissionChange(commissions1[commissionEl4], commissions1[commissionPercentEl4], commissions1[offerPrice4], 1)
        commissionChange(commissions1[commissionEl4], commissions1[commissionPercentEl4], commissions1[offerPrice4], 2)

    $('input[name="form-0-final_price"]').change(function(e){
        commissions[commissionEl] = $('input[name="form-0-commission"]');
        commissions[commissionPercentEl] = $('input[name="form-0-commission_percent"]');
        commissions[offerPrice] = $('input[name="form-0-final_price"]')

        commissionChange(commissions[commissionEl], commissions[commissionPercentEl], commissions[offerPrice], 2);

        commissionElbuyer = 'commissionElbuyer0'
        commissionPercentElbuyer = 'commissionPercentElbuyer0'
        offerPrice = 'offerPrice0'

        commissions1[commissionElbuyer] = $('input[name="form-0-commission_buyer"]');
        commissions1[commissionPercentElbuyer] = $('input[name="form-0-commission_buyer_percent"]'); 
        commissions1[offerPrice] = $('input[name="form-0-final_price"]')

        commissionChange(commissions1[commissionElbuyer], commissions1[commissionPercentElbuyer], commissions1[offerPrice], 2);
      
    })

    $('input[name="form-1-final_price"]').change(function(e){
        commissions[commissionEl] = $('input[name="form-1-commission"]');
        commissions[commissionPercentEl] = $('input[name="form-1-commission_percent"]');
        commissions[offerPrice] = $('input[name="form-1-final_price"]')

        commissionChange(commissions[commissionEl], commissions[commissionPercentEl], commissions[offerPrice], 2);

        commissionElbuyer = 'commissionElbuyer1'
        commissionPercentElbuyer = 'commissionPercentElbuyer1'
        offerPrice = 'offerPrice1'

        commissions1[commissionElbuyer] = $('input[name="form-1-commission_buyer"]');
        commissions1[commissionPercentElbuyer] = $('input[name="form-1-commission_buyer_percent"]'); 
        commissions1[offerPrice] = $('input[name="form-1-final_price"]')

        commissionChange(commissions1[commissionElbuyer], commissions1[commissionPercentElbuyer], commissions1[offerPrice], 2);
      
    })
}

var commissions_demand = {}

var commissionEl = 'commissionElbuyer'
var commissionPercentEl = 'commissionPercentElbuyer'
var offerPrice = 'offerPrice'

commissions_demand[commissionEl] = $('input[name="commission"]')
commissions_demand[commissionPercentEl] = $('input[name="commission_percent"]')

commissions_demand[offerPrice] = $('input[name="final_price"]')


commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 0)
commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 1)
commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 2)

var commissionEl = 'commissionElbuyer'
var commissionPercentEl = 'commissionPercentElbuyer'
var offerPrice = 'offerPrice'

commissions_demand[commissionEl] = $('input[name="commission_buyer"]')
commissions_demand[commissionPercentEl] = $('input[name="commission_buyer_percent"]')

commissions_demand[offerPrice] = $('input[name="final_price"]')


commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 0)
commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 1)
commissionChange(commissions_demand[commissionEl], commissions_demand[commissionPercentEl], commissions_demand[offerPrice], 2)