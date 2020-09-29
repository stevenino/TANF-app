import React from 'react'
import { render, fireEvent } from '@testing-library/react'

import Button from './Button.tsx'

describe('Button component', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders without errors', () => {
    const { queryByTestId } = render(<Button type="button">Click Me</Button>)
    expect(queryByTestId('button')).toBeInTheDocument()
  })

  describe('renders uswds classes', () => {
    it('usa-button', () => {
      const { queryByTestId } = render(<Button type="button">Click Me</Button>)
      expect(queryByTestId('button')).toHaveClass('usa-button')
    })

    const optionalBooleanClasses = [
      ['secondary', 'usa-button--secondary'],
      ['base', 'usa-button--base'],
      ['accent', 'usa-button--accent-cool'],
      ['outline', 'usa-button--outline'],
      ['inverse', 'usa-button--inverse'],
      ['unstyled', 'usa-button--unstyled'],
    ]

    optionalBooleanClasses.map((data) => {
      it(`${data[1]}`, () => {
        const additionalProps = {}
        additionalProps[data[0]] = true

        const { queryByTestId } = render(
          <Button type="button" {...additionalProps}>
            Click Me
          </Button>
        )
        expect(queryByTestId('button')).toHaveClass(data[1])
      })
    })

    it('renders uswds class for size big', () => {
      const { queryByTestId } = render(
        <Button type="button" size="big">
          Click Me
        </Button>
      )
      expect(queryByTestId('button')).toHaveClass('usa-button--big')
    })
  })

  it('implements an onClick handler', () => {
    const onClickFn = jest.fn()
    const { getByText } = render(
      <Button type="button" onClick={onClickFn}>
        Click Me
      </Button>
    )

    fireEvent.click(getByText('Click Me'))
    expect(onClickFn).toHaveBeenCalledTimes(1)
  })

  it('accepts additional custom class names', () => {
    const { getByTestId } = render(
      <Button className="customClass" type="button">
        Click Me
      </Button>
    )
    expect(getByTestId('button')).toHaveClass('usa-button')
    expect(getByTestId('button')).toHaveClass('customClass')
  })
})
