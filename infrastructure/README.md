# Terraform


To work with pre-defined scripts, move to the `aws` directory.
```bash
cd infrastructure/aws
```


Plan changes
```shell
./terraform.sh aws-profile-name plan
```


Apply changes
```shell
./terraform.sh aws-profile-name apply
```


Import to state
```shell
./import.sh aws-profile-name module.module-name module-id
```


Operations with state
```shell
./state.sh aws-profile-name mv 'module'.'module-name' 'module'.'module-new-name' 
```
