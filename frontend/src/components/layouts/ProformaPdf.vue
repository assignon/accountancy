<template>
    <div class='proforma-core'>
        <div class='pdf-header'>
            <div class='header-text'>
                <h2 style='color:#1976d2;'>CHICAM</h2>
                <p class='font-weight-bold'>TEL. 675 22 04 91 / 679 59 80 73 / 651 12 25 79</p>
                <p class='font-weight-bold'>Dealers in brand new tyres of all dimensions</p>
                <p class='font-weight-bold'>No contribuable: M111812730146E BP3629 YAOUNDE</p>
                <p class='font-weight-bold'>Import & Export commerce general</p>
            </div>
            <p style='position:relative;top:10px; width:20%'>
                <span class='font-weight-bold'>Date</span><br>
                {{new Date().toDateString()}}
            </p>
        </div>
        <div class='divider'></div>
        <div class='pdf-body'>
            <div class='details-container'>
                <div class='product-details'>
                    <h3>Product</h3>
                    <p>Size: {{$store.state.product.proSize}}</p>
                    <p>Price: {{formatPrice($store.state.product.proPrice)}}FRS</p>
                    <p>Vehicule: {{$store.state.product.proVehicle}}</p>
                </div>
                <div class='brands-details mt-5'>
                    <h3>Brands</h3>
                    <div class='brands'>
                        <p v-for='(brand, b) in $store.state.product.proBrands' :key="b">{{brand}}<span class='ml-2'></span></p>
                    </div>
                </div>
                <div class='profiles-details mt-3'>
                    <h3>Profiles</h3>
                    <div class='profiles'>
                        <p v-for='(profile, p) in $store.state.product.proProfiles' :key="p">{{profile}}<span class='ml-2'></span></p>
                    </div>
                </div>
            </div>
        </div>
        <div class='action-btn-container pb-3'>
            <v-btn large color='#1976d2' class='action-btn' style='color:white;text-transform:capitalize;font-weight:bold;' @click='reloadPAge()'>Back</v-btn>
            <v-btn large color='#1976d2' class='action-btn' style='color:white;text-transform:capitalize;font-weight:bold;' @click='printProforma()'>Print PDF</v-btn>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Proforma',

    data(){
        return{

        }
    },

    create(){},

    methods: {
        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") 
        },
        reloadPAge(){
            window.location.reload()
        },

        printProforma(){
            let actionBtn = document.querySelectorAll('.action-btn')
            for (let i = 0; i < actionBtn.length; i++) {
                const elem = actionBtn[i];
                elem.style.display = 'None'
            }
            
            setTimeout(() => {
                if (window.print) {
                    window.print(0);
                    window.location.reload()
                } else {
                    alert("your browser doesn't support this function")
                }
            }, 10);
        },

        parseDate(date){
            return new Date(date).toDateString()
        },
    }
}
</script>

<style scoped>
    ::-webkit-scrollbar {
         width: 0px;
    }
    .proforma-core{
        width: 100%;
        height: 100vh;
        margin-bottom: 50px;
        overflow-y: scroll;
        overflow-x: hidden;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: #fff;
        background-image: url('../../assets/chicam.jpg');
        background-size: 50%;
        background-position: center;
        background-repeat: no-repeat;
    }
    .pdf-header{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 50px;
    }
    .header-text{
        height: auto;
        width: 80%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .divider{
        width: 100%;
        border: 0.5px solid #1e1d2b;
    }
    .pdf-body{
        width: 100%;
        height: 70%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin-top: 20px;
        margin-bottom: 20px;
    }
     .details-container{
        height: 90%;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .product-details, .brands-details, .profiles-details{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .product-details h3, .brands-details h3, .profiles-details h3{
        color: #1976d2;
        text-align: left;
    }
    .product-details p, .brands-details p, .profiles-details p{
         color: #1e1d2b;
        text-align: left;
        font-size:18px;
        text-align: left;
        margin: 0px;
        padding: 0px;
        text-transform: capitalize;
    }
    .action-btn-container{
        width: 50%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 10px;
    }
</style>