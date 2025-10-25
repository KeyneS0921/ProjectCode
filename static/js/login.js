function handleLogin(event) {
    event.preventDefault();
  
    const role = document.querySelector('input[name="role"]:checked');
    
    if (!role) {
      alert('Please select a role.');
      return;
    }
  
    const selectedRole = role.value;
  
    if (selectedRole === 'customer') {
      window.location.href = 'menu_customer.html';
    } else if (selectedRole === 'merchant') {
      window.location.href = 'merchant_dashboard.html';
    }
  }
  