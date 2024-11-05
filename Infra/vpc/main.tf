resource "aws_vpc" "DevOps_infra" {
  cidr_block = var.cidr_block

  tags = {
    Department = "DevOps_infra"
  }
}



resource "aws_subnet" "public_subnets" {
  count      = length(var.public_subnet_cidrs)
  vpc_id     = aws_vpc.DevOps_infra.id
  cidr_block = element(var.public_subnet_cidrs, count.index)

  tags = {
    Name = "DevOps_infra ${count.index + 1}"
  }
}

resource "aws_subnet" "private_subnets" {
  count      = length(var.private_subnet_cidrs)
  vpc_id     = aws_vpc.DevOps_infra.id
  cidr_block = element(var.private_subnet_cidrs,count.index)
  tags = {
    Name = "DevOps_infra ${count.index + 1}"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.DevOps_infra.id

  tags = {
    Department = "DevOps_infra"
    Name       = "igw"
  }
}


resource "aws_eip" "nat" {
  vpc = true

  tags = {
    Name       = "nat"
    Department = "DevOps infra"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnets[1].id

  tags = {
    Name       = "de_nat"
    Department = "DevOps infra"
  }

  depends_on = [aws_internet_gateway.igw]
}


resource "aws_route_table" "public_subnet_rt" {
  vpc_id = aws_vpc.DevOps_infra.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Department = "DevOps_infra"
    Name       = "Public Route table"
  }
}

resource "aws_route_table" "private_subnet_rt" {
  vpc_id = aws_vpc.DevOps_infra.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.nat.id
  }
  tags = {
    Department = "DevOps_infra"
    Name       = "Private Route Table"
  }
}


resource "aws_route_table_association" "public_subnet_asso" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = element(aws_subnet.public_subnets[*].id, count.index)
  route_table_id = aws_route_table.public_subnet_rt.id
}

resource "aws_route_table_association" "private_subnet_asso" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = element(aws_subnet.private_subnets[*].id, count.index)
  route_table_id = aws_route_table.private_subnet_rt.id
}