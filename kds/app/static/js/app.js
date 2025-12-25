const socket = io();


socket.on('new_order', () => location.reload());
socket.on('update', () => location.reload());


function done(id){
fetch(`/item/${id}/done`, {method:'POST'})
}
function serve(id){
fetch(`/order/${id}/served`, {method:'POST'})
}

function addItem() {
  const row = document.createElement("div");
  row.className = "item-row";

  row.innerHTML = `
    <input type="text" name="name[]" placeholder="Food name" required>
    <select name="section[]">
      <option value="fry">Fry</option>
      <option value="grill">Grill</option>
      <option value="salad">Salad</option>
      <option value="dessert">Dessert</option>
      <option value="beverage">Beverage</option>
      <option value="pizza">Pizza</option>
    </select>
  `;

  document.getElementById("items").appendChild(row);
}

