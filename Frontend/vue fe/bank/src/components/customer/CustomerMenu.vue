<template>
    <nav id="customerSidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
        <div class="position-sticky pt-3">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/myloans" class="nav-link" active-class="active">
                        Loans
                    </router-link>
                    <router-link to="/createloan" class="nav-link" active-class="active">
                        Create Loan
                    </router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    name: "CustomerMenu",
};
</script>
