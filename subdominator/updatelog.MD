# Subdominator V2.0.0 Update Log

## What's New?

We are excited to introduce **Subdominator V2.0.0**, featuring additional minor updates, bug fixes, and significant changes in the `rsecloud` resource handling and `dnsdumpster` API key configuration.

### Bug Fixes & Enhancements:

**Resolved Performance Issue in `rsecloud` Resource:**  
- A critical performance bug was identified in **Subdominator** where, upon reaching 100% of the API usage limit for `rsecloud`, the tool sent infinite requests due to an unhandled response. This caused severe performance degradation.
- This issue was verified during internal testing and also reported as [Issue #20](https://github.com/RevoltSecurities/Subdominator/issues/20).  
- Subdominator V2.0.0 addresses this problem by introducing proper response handling, preventing unnecessary request loops.

### `dnsdumpster` Configuration Changes:

Setting up **dnsdumpster** with its API keys has been simplified in this release. Follow these steps to configure it seamlessly:

1. Visit the [dnsdumpster website](https://dnsdumpster.com) and register a new account.  
2. After registering, navigate to your account dashboard to find your API key under the [My Account](https://dnsdumpster.com/my-account/) section.  
3. Copy your API key(s) and paste them into the YAML configuration file as shown below:  

    ```yaml
    dnsdumpster:
        - z4gi42ifs9asdjbopakwbhorhao0du42po92jkbnkjbsdug082sjbkdhohabdaoiuboadhg
        - jdbsaoug0242kjblas42po92jkbnkjbsdug082sjbkdhohabadsjbudaugiuga98t24vi2u
    ```

4. Once updated, Subdominator will run smoothly without any exceptions related to `dnsdumpster` API configurations.

With these updates, **Subdominator V2.0.0** ensures better performance, reliability, and ease of use.