<template>
    <nav id="bankerSidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
        <div class="position-sticky pt-3">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/pending-loans" class="nav-link" active-class="active">
                        Pending Loans
                    </router-link>
                    <router-link to="/pending-funds" class="nav-link" active-class="active">
                        Pending Funds
                    </router-link>
                    <router-link to="/create-loan-option" class="nav-link" active-class="active">
                        Create Loan Option
                    </router-link>
                    <router-link to="/create-fund-option" class="nav-link" active-class="active">
                        Create Fund Option
                    </router-link>
                    <router-link to="/system-report" class="nav-link" active-class="active">
                        System Report
                    </router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    name: "BankerMenu",
};
</script>
