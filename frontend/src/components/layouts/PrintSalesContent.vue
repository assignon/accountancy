<template>
    <div class='pdf-core'>
        <div class='pdf-header'>
            <div class='header-text' v-if='data.length>0'>
                <h2>CHICAM</h2>
                <p class='font-weight-bold'>TEL. 675 22 04 91 / 679 59 80 73 / 651 12 25 79</p>
                <p class='font-weight-bold'>Dealers in brand new tyres of all dimensions</p>
                <p class='font-weight-bold'>No contribuable: M111812730146E BP3629 YAOUNDE</p>
                <p class='font-weight-bold'>Import & Export commerce general</p>
            </div>
            <p style='position:relative;top:10px; width:20%' v-if='data.length>0'>
                <span class='font-weight-bold'>Date</span><br>
                {{new Date().toDateString()}}
            </p>
        </div>
        <div class='order-content' v-for='(order, i) in data' :key='i'>
            <div class='separator'></div>
            <div class='pdf-body'>
                <div class='customer-info-flex'>
                    <h3 class='mb-5' style='color:#1976d2'>Customer Information</h3>
                    <div class='info-format'>
                        <p class='font-weight-bold mb-1 pr-2'>Name:</p>
                        <p class='mb-3'>{{order.credential[0].name}}</p>
                    </div>
                    <div class='info-format' v-if='order.credential[0].email!=null'>
                        <p class='font-weight-bold mb-1 pr-2'>Email:</p>
                        <p class='mb-3'>{{order.credential[0].email}}</p>
                    </div>
                    <div class='info-format' v-if='order.credential[0].address!=null'>
                        <p class='font-weight-bold mb-1 pr-2'>Address:</p>
                        <p class='mb-3'>{{order.credential[0].address}}</p>
                    </div>
                    <div class='info-format' v-if='order.credential[0].tel_number!=null'>
                        <p class='font-weight-bold mb-1 pr-2'>Tel. Number:</p>
                        <p class='mb-3'>{{order.credential[0].tel_number}}</p>
                    </div>
                </div>

                <div class='payment-flex'>
                    <h3 class='mb-5' style='color:#1976d2'>Payments Method</h3>
                    <div class='info-format'>
                        <p class='font-weight-bold mb-1 pr-2'>Start Date:</p>
                        <p class='mb-3'>{{order.customer[0].start}}</p>
                    </div>
                    <div class='info-format'>
                        <p class='font-weight-bold mb-1 pr-2'>Pay In:</p>
                        <p class='mb-3'>{{order.payment[0].pay_in}}</p>
                    </div>
                    <div class='info-format'>
                        <p class='font-weight-bold mb-1 pr-2'>Payment Interval:</p>
                        <p class='mb-3'>{{order.payment[0].payment_interval}}</p>
                    </div>
                    <div class='info-format'>
                        <p class='font-weight-bold pr-2' mb-1>Method:</p>
                        <p class='mb-3'>{{order.method[0].name}}</p>
                    </div>
                    <div class='info-format'>
                        <p class='font-weight-bold pr-2' mb-1>paying in terms:</p>
                        <p class='mb-3'>{{formatPrice(order.payment_helper.paying_in_terms)}}FRS</p>
                    </div>
                </div>
            </div>
            <div class='divider'></div>
            <div class='pdf-footer'>
                <h3 class='mb-5 mt-5' style='color:#1976d2'>Orders</h3>
                <div class='info-format'>
                    <p class='font-weight-bold pr-2'>Order Place on:</p>
                    <p>{{parseDate(order.order.order_on)}}</p>
                </div>
                <table class='order-table mt-5'>
                    <tr>
                        <th>Size</th>
                        <th>Brands</th>
                        <th>Vehical</th>
                        <th>Profiles</th>
                        <th>Price</th>
                        <th>Quantity</th>
                    </tr>
                    <tr v-for="(product,p) in order.products" :key="p" >
                        <td>{{product.product[0].size}}</td>
                        <td v-if=' product.brands.length>0'>
                            <p v-for="(brand, b) in product.brands" :key="b">{{brand.name}}</p>
                        </td>
                        <td v-else>
                            <p>None</p>
                        </td>
                        <td v-if='product.vehicule.length>0'>{{product.vehicule[0].name}}</td>
                        <td v-else>None</td>
                        <td v-if='product.profiles.length>0'>
                            <p v-for="(profile, p) in product.profiles" :key="p">{{profile.name}}</p>
                        </td>
                        <td v-else>
                            <p>None</p>
                        </td>
                        <td v-if='product.ordered_product[0].custome_price==0'>{{formatPrice(product.product[0].price)}}FRS</td>
                        <td v-else>{{formatPrice(product.ordered_product[0].custome_price)}}FRS</td>
                        <td>{{product.ordered_product[0].quantity}}</td>
                    </tr>
                </table>

                <h3 class='mt-3'>
                    <!-- <span style='color: #1976d2;'>Total Price: {{formatPrice(order.paying)}}FRS</span> -->
                    <span style='color: #1976d2;'>Total Price: {{formatPrice(order.payment_helper.paying_in_terms)}}FRS</span>
                </h3>

            </div>
        </div>
    </div>
</template>

<script>
// import { mapGetters } from 'vuex';
export default {
    name: 'OrderPDF',

    props: ['data'],

    // computed: {
    //     ...mapGetters({
    //         orderDeteails: 'order/getCustomerOrder',
    //     }),
    // },

    created(){
        
    },

    methods: {
        formatPrice(value) {
            let val = (value/1).toFixed(0).replace('.', ',')
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        },

        reloadPAge(){
            window.location.reload()
        },

        parseDate(date){
            return new Date(date).toDateString()
        },
    }
}

</script>

<style scoped>
    :-webkit-scrollbar {
         width: 0px;
    }
    .pdf-core{
        width: 100%;
        min-height: auto;
        height: auto;
        margin-bottom: 50px;
        overflow-y: scroll;
        overflow-x: hidden;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        /* overflow-y: scroll; */
        /* background-color: #fff;
        background-image: url('../../assets/chicam.jpg');
        background-size: 20%;
        background-position: 40%;
        background-repeat: no-repeat; */
    }
    .pdf-header{
        height: auto;
        width: 90%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 50px;
    }
    .header-text{
        height: auto;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .order-content{
        width: 90%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-start;
        background-color: #fff;
        background-image: url('../../assets/chicam.jpg');
        background-size: 20%;
        background-position: 40%;
        background-repeat: no-repeat;
        margin-bottom: 50px;
    }
    .pdf-body{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-start;
        margin-top: 50px;
        margin-bottom: 50px;
    }
    .customer-info-flex{
        width: auto;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .payment-flex{
        width: auto;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .info-format{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .pdf-core h2, .pdf-core h2{
        color: #1976d2;
        text-align: left;
    }
    .pdf-core h3{
        color: #15141c;
    }
    .pdf-core p{
        color: #15141c;
        font-size:18px;
        text-align: left;
        margin: 0px;
        padding: 0px;
        /* background-color: white; */
        text-transform: capitalize;
    }
    .pdf-footer{
        width: 100%;
        height: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
    }
    .order-table{
        width: 80%;
    }
    .order-table, th, td {
        border: 1px solid #1e1d2b;
        border-collapse: collapse;
        color: #1e1d2b;
        padding: 5px 20px 5px 20px;
        font-size: 17px;
        text-align: left;
    }
    .order-table, td p{
        color: #1e1d2b;
    }
    .total-price{
        width: 80%;
        height: auto;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 10px;
    }
    .divider{
        width: 100%;
        border: 0.5px solid #1e1d2b;
    }
    .separator{
        width: 100%;
        border: 2px solid #1976d2;
        background-color: #1976d2;
    }
    
    @media print {
  *,
  *::before,
  *::after {
    text-shadow: none !important;
    box-shadow: none !important;
  }

  a:not(.btn) {
    text-decoration: underline;
  }

  abbr[title]::after {
    content: " (" attr(title) ")";
  }

  pre {
    white-space: pre-wrap !important;
  }

  pre,
  blockquote {
    border: 1px solid #adb5bd;
    page-break-inside: avoid;
  }

  thead {
    display: table-header-group;
  }

  tr,
  img {
    page-break-inside: avoid;
  }

  p,
  h2,
  h3 {
    orphans: 3;
    widows: 3;
  }

  h2,
  h3 {
    page-break-after: avoid;
  }

  @page {
    size: a3;
  }
}

</style>