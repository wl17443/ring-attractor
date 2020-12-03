using DrWatson
@quickactivate

include(srcdir("utils.jl"))
function testWM()

	w = WeightMatrix()
	w[1, 1] = 1.
	@test w[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] = -1.
	@test w[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += 1.
	@test w[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += -1.
	@test w[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= 1.
	@test w[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= -1.
	@test w[1, 1] == 0.

	w = WeightMatrix()
	w[1, 1] = 1.
	@test w.i[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] = -1.
	@test w.i[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += 1.
	@test w.i[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += -1.
	@test w.i[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= 1.
	@test w.i[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= -1.
	@test w.i[1, 1] == 0.

	w = WeightMatrix()
	w[1, 1] = 1.
	@test w.e[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] = -1.
	@test w.e[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += 1.
	@test w.e[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] += -1.
	@test w.e[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= 1.
	@test w.e[1, 1] == 0.
	w = WeightMatrix()
	w[1, 1] -= -1.
	@test w.e[1, 1] == 0.

	w = WeightMatrix()
	w[1, 2] = 1.
	@test w[1, 2] == 1.
	w = WeightMatrix()
	w[1, 2] = -1.
	@test w[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] += 1.
	@test w[1, 2] == 1.05
	w = WeightMatrix()
	w[1, 2] += -1.
	@test w[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] -= 1.
	@test w[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] -= -1.
	@test w[1, 2] == 1.05

	w = WeightMatrix()
	w[1, 2] = 1.
	@test w.i[1, 2] == 0.
	w = WeightMatrix()
	w[1, 2] = -1.
	@test w.i[1, 2] == 0.
	w = WeightMatrix()
	w[1, 2] += 1.
	@test w.i[1, 2] == 0.
	w = WeightMatrix()
	w[1, 2] += -1.
	@test w.i[1, 2] == 0.
	w = WeightMatrix()
	w[1, 2] -= 1.
	@test w.i[1, 2] == 0.
	w = WeightMatrix()
	w[1, 2] -= -1.
	@test w.i[1, 2] == 0.

	w = WeightMatrix()
	w[1, 2] = 1.
	@test w.e[1, 2] == 1.
	w = WeightMatrix()
	w[1, 2] = -1.
	@test w.e[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] += 1.
	@test w.e[1, 2] == 1.05
	w = WeightMatrix()
	w[1, 2] += -1.
	@test w.e[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] -= 1.
	@test w.e[1, 2] == 0.05
	w = WeightMatrix()
	w[1, 2] -= -1.
	@test w.e[1, 2] == 1.05

	w = WeightMatrix()
	w[7, 1] = 1.
	@test w[7, 1] == 1.
	w = WeightMatrix()
	w[7, 1] = -1.
	@test w[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] += 1.
	@test w[7, 1] == 1.1
	w = WeightMatrix()
	w[7, 1] += -1.
	@test w[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] -= 1.
	@test w[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] -= -1.
	@test w[7, 1] == 1.1

	w = WeightMatrix()
	w[7, 1] = 1.
	@test w.e[7, 1] == 0.
	w = WeightMatrix()
	w[7, 1] = -1.
	@test w.e[7, 1] == 0.
	w = WeightMatrix()
	w[7, 1] += 1.
	@test w.e[7, 1] == 0.
	w = WeightMatrix()
	w[7, 1] += -1.
	@test w.e[7, 1] == 0.
	w = WeightMatrix()
	w[7, 1] -= 1.
	@test w.e[7, 1] == 0.
	w = WeightMatrix()
	w[7, 1] -= -1.
	@test w.e[7, 1] == 0.

	w = WeightMatrix()
	w[7, 1] = 1.
	@test w.i[7, 1] == 1.
	w = WeightMatrix()
	w[7, 1] = -1.
	@test w.i[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] += 1.
	@test w.i[7, 1] == 1.1
	w = WeightMatrix()
	w[7, 1] += -1.
	@test w.i[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] -= 1.
	@test w.i[7, 1] == 0.1
	w = WeightMatrix()
	w[7, 1] -= -1.
	@test w.i[7, 1] == 1.1
end
