<template>
    <nav id="funderSidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
        <div class="position-sticky pt-3">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/myfunds" class="nav-link" active-class="active">
                        Funds
                    </router-link>
                    <router-link to="/createfund" class="nav-link" active-class="active">
                        Create Fund
                    </router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    name: "FunderMenu",
};
</script>
